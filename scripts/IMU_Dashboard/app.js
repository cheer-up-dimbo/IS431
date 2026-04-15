// CDE4301 IMU Validation Dashboard Logic

// State
let socket;
let isConnected = false;
let isRecording = false;
let recordedData = [];
let startTime = 0;

// Calibration Offsets
let offsets = { ax: 0, ay: 0, az: 0, gx: 0, gy: 0, gz: 0 };
let calibrating = false;
let calibBuffer = { count: 0, ax: 0, ay: 0, az: 0, gx: 0, gy: 0, gz: 0 };

// Strike Calculation State
let velocity = 0;
let lastTime = null;
let peakAccel = 0;
const ACCEL_THRESHOLD = 0.5; // g - ignore values below this after calibration to prevent integration drift.

// Shakiness Buffer (Variance calculation)
const shakeBuffer = [];
const SHAKE_WINDOW = 50; // packets

// DOM Elements
const statusIndicator = document.getElementById('connectionStatus');
const btnConnect = document.getElementById('btnConnect');
const btnCalibrate = document.getElementById('btnCalibrate');
const btnRecord = document.getElementById('btnRecord');
const btnExport = document.getElementById('btnExport');

const domStrike = document.getElementById('strikeVal');
const domPeak = document.getElementById('peakAccelVal');
const domRot = document.getElementById('rotationVal');
const domShake = document.getElementById('shakeVal');
const domPitch = document.getElementById('pitchVal');
const domRoll = document.getElementById('rollVal');

// Chart Setup
const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false, // Turn off animation for realtime performance
    plugins: {
        legend: { labels: { color: '#f8f9fa' } }
    },
    scales: {
        x: { display: false },
        y: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#8b92a5' } }
    },
    elements: {
        point: { radius: 0 },
        line: { tension: 0.1, borderWidth: 2 }
    }
};

const accelCtx = document.getElementById('accelChart').getContext('2d');
const accelChart = new Chart(accelCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Accel X (g)', borderColor: '#ff4b4b', data: [] },
            { label: 'Accel Y (g)', borderColor: '#00ff87', data: [] },
            { label: 'Accel Z (g)', borderColor: '#00d2ff', data: [] }
        ]
    },
    options: commonOptions
});

const gyroCtx = document.getElementById('gyroChart').getContext('2d');
const gyroChart = new Chart(gyroCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Gyro X (dps)', borderColor: '#ff4b4b', data: [] },
            { label: 'Gyro Y (dps)', borderColor: '#00ff87', data: [] },
            { label: 'Gyro Z (dps)', borderColor: '#b050ff', data: [] }
        ]
    },
    options: commonOptions
});

const MAX_POINTS = 100;

function updateCharts(t, ax, ay, az, gx, gy, gz) {
    accelChart.data.labels.push(t);
    accelChart.data.datasets[0].data.push(ax);
    accelChart.data.datasets[1].data.push(ay);
    accelChart.data.datasets[2].data.push(az);

    gyroChart.data.labels.push(t);
    gyroChart.data.datasets[0].data.push(gx);
    gyroChart.data.datasets[1].data.push(gy);
    gyroChart.data.datasets[2].data.push(gz);

    if (accelChart.data.labels.length > MAX_POINTS) {
        accelChart.data.labels.shift();
        for (let i = 0; i < 3; i++) {
            accelChart.data.datasets[i].data.shift();
            gyroChart.data.datasets[i].data.shift();
        }
        gyroChart.data.labels.shift();
    }
    
    accelChart.update();
    gyroChart.update();
}

function calculateVariance(arr) {
    if (arr.length === 0) return 0;
    const mean = arr.reduce((a, b) => a + b) / arr.length;
    return arr.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / arr.length;
}

function processData(rawRaw) {
    let raw = { ...rawRaw };

    if (calibrating) {
        calibBuffer.ax += raw.ax; calibBuffer.ay += raw.ay; calibBuffer.az += raw.az;
        calibBuffer.gx += raw.gx; calibBuffer.gy += raw.gy; calibBuffer.gz += raw.gz;
        calibBuffer.count++;
        return; // Don't process while gathering baseline
    }

    // Apply offset
    let ax = raw.ax - offsets.ax;
    let ay = raw.ay - offsets.ay;
    let az = raw.az - offsets.az;
    let gx = raw.gx - offsets.gx;
    let gy = raw.gy - offsets.gy;
    let gz = raw.gz - offsets.gz;

    let currentTime = raw.t / 1000.0; // Assume time is in ms

    // 1. STRIKE VELOCITY (m/s)
    let accelMagnitude = Math.sqrt(ax*ax + ay*ay + az*az);
    if (accelMagnitude > peakAccel) peakAccel = accelMagnitude;
    
    if (lastTime !== null) {
        let dt = currentTime - lastTime;
        // Basic integration V = V0 + A * dt
        if (accelMagnitude > ACCEL_THRESHOLD) {
            velocity += (accelMagnitude * 9.81) * dt;
        } else {
            // Decay velocity slowly if no acceleration 
            velocity *= 0.95;
            if (velocity < 0.05) velocity = 0;
        }
    }
    lastTime = currentTime;

    // 2. BASE ROTATION (RPM)
    let rpmZ = gz / 6.0;

    // 3. TILT (Pitch/Roll) & SHAKINESS
    // Tilt calculated from raw to keep gravity dependence
    let roll = Math.atan2(raw.ay, raw.az) * 180 / Math.PI;
    let pitch = Math.atan2(-raw.ax, Math.sqrt(raw.ay * raw.ay + raw.az * raw.az)) * 180 / Math.PI;

    // Shakiness: Variance of the magnitude
    shakeBuffer.push(accelMagnitude);
    if (shakeBuffer.length > SHAKE_WINDOW) shakeBuffer.shift();
    let variance = calculateVariance(shakeBuffer);

    // Update UI
    domStrike.innerText = velocity.toFixed(2);
    domPeak.innerText = peakAccel.toFixed(2);
    domRot.innerText = Math.abs(rpmZ).toFixed(0);
    domShake.innerText = variance.toFixed(3);
    domPitch.innerText = pitch.toFixed(1) + '°';
    domRoll.innerText = roll.toFixed(1) + '°';

    // Update Charts
    updateCharts(currentTime.toFixed(1), ax, ay, az, gx, gy, gz);

    // Record dataset if active
    if (isRecording) {
        recordedData.push({
            time_ms: raw.t,
            ax: raw.ax, ay: raw.ay, az: raw.az,
            gx: raw.gx, gy: raw.gy, gz: raw.gz,
            calibrated_ax: ax, calibrated_ay: ay, calibrated_az: az,
            velocity_m_s: velocity,
            rotation_rpm: rpmZ,
            pitch_deg: pitch,
            roll_deg: roll,
            shake_variance: variance
        });
    }
}

// WebSocket Event Handlers
function connectWS() {
    if (isConnected) {
        socket.close();
        return;
    }

    // Connect to Arduino IP
    socket = new WebSocket('ws://192.168.4.1:81');

    socket.onopen = () => {
        isConnected = true;
        statusIndicator.innerText = "Connected";
        statusIndicator.className = "status-indicator connected";
        btnConnect.innerText = "Disconnect";
        velocity = 0;
        peakAccel = 0;
    };

    socket.onmessage = (event) => {
        try {
            let data = JSON.parse(event.data);
            processData(data);
        } catch (e) {
            console.error("Parse Error:", e);
        }
    };

    socket.onclose = () => {
        isConnected = false;
        statusIndicator.innerText = "Disconnected";
        statusIndicator.className = "status-indicator disconnected";
        btnConnect.innerText = "Connect";
    };

    socket.onerror = (error) => {
        console.error("WS Error:", error);
    };
}

// Listeners
btnConnect.addEventListener('click', connectWS);

btnCalibrate.addEventListener('click', () => {
    btnCalibrate.innerText = "Calibrating...";
    btnCalibrate.disabled = true;
    calibrating = true;
    
    calibBuffer = { count: 0, ax: 0, ay: 0, az: 0, gx: 0, gy: 0, gz: 0 };
    velocity = 0; 
    peakAccel = 0;

    // Collect 1 second baseline
    setTimeout(() => {
        if (calibBuffer.count > 0) {
            offsets.ax = calibBuffer.ax / calibBuffer.count;
            offsets.ay = calibBuffer.ay / calibBuffer.count;
            offsets.az = calibBuffer.az / calibBuffer.count;
            offsets.gx = calibBuffer.gx / calibBuffer.count;
            offsets.gy = calibBuffer.gy / calibBuffer.count;
            offsets.gz = calibBuffer.gz / calibBuffer.count;
        }
        calibrating = false;
        btnCalibrate.innerText = "Calibrate (0g)";
        btnCalibrate.disabled = false;
        console.log("Calibrated Offsets:", offsets);
    }, 1000);
});

btnRecord.addEventListener('click', () => {
    if (isRecording) {
        isRecording = false;
        btnRecord.innerText = "Start Record";
        btnRecord.classList.remove("primary");
        btnRecord.classList.add("secondary");
        btnExport.disabled = false;
    } else {
        recordedData = [];
        isRecording = true;
        btnRecord.innerText = "Stop Recording";
        btnRecord.classList.remove("secondary");
        btnRecord.classList.add("primary");
        btnExport.disabled = true;
    }
});

btnExport.addEventListener('click', () => {
    if (recordedData.length === 0) {
        alert("No data recorded!");
        return;
    }

    const headers = Object.keys(recordedData[0]).join(",");
    const rows = recordedData.map(obj => Object.values(obj).join(",")).join("\n");
    const csvContent = headers + "\n" + rows;

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `IMU_Validation_Data_${new Date().getTime()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});
