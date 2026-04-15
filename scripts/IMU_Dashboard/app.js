// CDE4301 IMU Validation Dashboard Logic - HIGH PERFORMANCE BLE VERSION

// State
let isConnected = false;
let isRecording = false;
let recordedData = [];

// BLE State
let bleDevice;
let bleCharacteristic;

// Calibration Offsets
let offsets = { ax: 0, ay: 0, az: 0, gx: 0, gy: 0, gz: 0 };
let calibrating = false;
let calibBuffer = { count: 0, ax: 0, ay: 0, az: 0, gx: 0, gy: 0, gz: 0 };

// Global Metrics State (for the render loop)
let velocity = 0;
let lastTime = null;
let peakAccel = 0;
let rpmZ = 0;
let pitch = 0;
let roll = 0;
let variance = 0;
const ACCEL_THRESHOLD = 0.5;

// Shakiness Buffer
const shakeBuffer = [];
const SHAKE_WINDOW = 50;

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
    animation: false, // CRITICAL for performance
    normalized: true, // CRITICAL for high-speed data parsing
    plugins: { legend: { labels: { color: '#f8f9fa' } } },
    scales: {
        x: { display: false },
        y: { grid: { color: 'rgba(255, 255, 255, 0.1)' }, ticks: { color: '#8b92a5' } }
    },
    elements: { point: { radius: 0 }, line: { tension: 0.1, borderWidth: 2 } }
};

const accelCtx = document.getElementById('accelChart').getContext('2d');
const accelChart = new Chart(accelCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Accel X', borderColor: '#ff4b4b', data: [] },
            { label: 'Accel Y', borderColor: '#00ff87', data: [] },
            { label: 'Accel Z', borderColor: '#00d2ff', data: [] }
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
            { label: 'Gyro X', borderColor: '#ff4b4b', data: [] },
            { label: 'Gyro Y', borderColor: '#00ff87', data: [] },
            { label: 'Gyro Z', borderColor: '#b050ff', data: [] }
        ]
    },
    options: commonOptions
});

const MAX_POINTS = 100;

// --- OPTIMIZATION 1: DATA INGESTION ---
// This handles math instantly, but does NOT touch the DOM or redraw charts
function processData(rawRaw) {
    let raw = { ...rawRaw };

    if (calibrating) {
        calibBuffer.ax += raw.ax; calibBuffer.ay += raw.ay; calibBuffer.az += raw.az;
        calibBuffer.gx += raw.gx; calibBuffer.gy += raw.gy; calibBuffer.gz += raw.gz;
        calibBuffer.count++;
        return; 
    }

    // Apply offset
    let ax = raw.ax - offsets.ax;
    let ay = raw.ay - offsets.ay;
    let az = raw.az - offsets.az;
    let gx = raw.gx - offsets.gx;
    let gy = raw.gy - offsets.gy;
    let gz = raw.gz - offsets.gz;

    let currentTime = raw.t / 1000.0; 

    // Calculations
    let accelMagnitude = Math.sqrt(ax*ax + ay*ay + az*az);
    if (accelMagnitude > peakAccel) peakAccel = accelMagnitude;
    
    if (lastTime !== null) {
        let dt = currentTime - lastTime;
        if (accelMagnitude > ACCEL_THRESHOLD) {
            velocity += (accelMagnitude * 9.81) * dt;
        } else {
            velocity *= 0.95;
            if (velocity < 0.05) velocity = 0;
        }
    }
    lastTime = currentTime;

    rpmZ = gz / 6.0;
    roll = Math.atan2(raw.ay, raw.az) * 180 / Math.PI;
    pitch = Math.atan2(-raw.ax, Math.sqrt(raw.ay * raw.ay + raw.az * raw.az)) * 180 / Math.PI;

    shakeBuffer.push(accelMagnitude);
    if (shakeBuffer.length > SHAKE_WINDOW) shakeBuffer.shift();
    
    // Fast variance calc
    const mean = shakeBuffer.reduce((a, b) => a + b, 0) / shakeBuffer.length;
    variance = shakeBuffer.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / shakeBuffer.length;

    // Push data to chart arrays (memory only, no rendering)
    accelChart.data.labels.push(currentTime.toFixed(1));
    accelChart.data.datasets[0].data.push(ax);
    accelChart.data.datasets[1].data.push(ay);
    accelChart.data.datasets[2].data.push(az);

    gyroChart.data.labels.push(currentTime.toFixed(1));
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

    if (isRecording) {
        recordedData.push({
            time_ms: raw.t,
            ax: raw.ax, ay: raw.ay, az: raw.az,
            gx: raw.gx, gy: raw.gy, gz: raw.gz,
            velocity_m_s: velocity, rotation_rpm: rpmZ,
            pitch_deg: pitch, roll_deg: roll, shake_variance: variance
        });
    }
}

// --- OPTIMIZATION 2: THE RENDER LOOP ---
// This runs 20 times a second independently of the Bluetooth data.
// It groups all UI updates together to prevent browser layout thrashing.
setInterval(() => {
    if (isConnected) {
        domStrike.innerText = velocity.toFixed(2);
        domPeak.innerText = peakAccel.toFixed(2);
        domRot.innerText = Math.abs(rpmZ).toFixed(0);
        domShake.innerText = variance.toFixed(3);
        domPitch.innerText = pitch.toFixed(1) + '°';
        domRoll.innerText = roll.toFixed(1) + '°';
        
        accelChart.update();
        gyroChart.update();
    }
}, 50); // 50ms = 20 FPS

// Web Bluetooth Logic
async function connectBLE() {
    if (isConnected) {
        if (bleDevice && bleDevice.gatt.connected) bleDevice.gatt.disconnect();
        return;
    }

    try {
        btnConnect.innerText = "Scanning...";
        bleDevice = await navigator.bluetooth.requestDevice({
            filters: [{ name: 'RobotIMU' }],
            optionalServices: ['19b10000-e8f2-537e-4f6c-d104768a1214']
        });

        bleDevice.addEventListener('gattserverdisconnected', onDisconnected);

        const server = await bleDevice.gatt.connect();
        const service = await server.getPrimaryService('19b10000-e8f2-537e-4f6c-d104768a1214');
        bleCharacteristic = await service.getCharacteristic('19b10001-e8f2-537e-4f6c-d104768a1214');

        bleCharacteristic.addEventListener('characteristicvaluechanged', handleNotifications);
        await bleCharacteristic.startNotifications();

        isConnected = true;
        statusIndicator.innerText = "BLE Connected";
        statusIndicator.className = "status-indicator connected";
        btnConnect.innerText = "Disconnect";
        velocity = 0;
        peakAccel = 0;

    } catch (error) {
        console.error("BLE Error:", error);
        btnConnect.innerText = "Connect";
    }
}

function handleNotifications(event) {
    const value = event.target.value;
    const decoder = new TextDecoder('utf-8');
    const parts = decoder.decode(value).split(',');
    
    if (parts.length === 7) {
        processData({
            t: parseInt(parts[0]),
            ax: parseFloat(parts[1]), ay: parseFloat(parts[2]), az: parseFloat(parts[3]),
            gx: parseFloat(parts[4]), gy: parseFloat(parts[5]), gz: parseFloat(parts[6])
        });
    }
}

function onDisconnected() {
    isConnected = false;
    statusIndicator.innerText = "Disconnected";
    statusIndicator.className = "status-indicator disconnected";
    btnConnect.innerText = "Connect";
}

// Listeners
btnConnect.addEventListener('click', connectBLE);

btnCalibrate.addEventListener('click', () => {
    btnCalibrate.innerText = "Calibrating...";
    btnCalibrate.disabled = true;
    calibrating = true;
    calibBuffer = { count: 0, ax: 0, ay: 0, az: 0, gx: 0, gy: 0, gz: 0 };
    velocity = 0; peakAccel = 0;

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
    if (recordedData.length === 0) return alert("No data recorded!");
    const headers = Object.keys(recordedData[0]).join(",");
    const rows = recordedData.map(obj => Object.values(obj).join(",")).join("\n");
    const blob = new Blob([headers + "\n" + rows], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `IMU_Data_${new Date().getTime()}.csv`;
    link.click();
});