// Simple ESP32 + MPU6050 punch sensor.
// Reads linear acceleration, prints magnitude to Serial, and tracks peak impact.

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Serial and sensor configuration
static constexpr int kSerialBaud = 115200;
static constexpr size_t kCalibrationSamples = 500;  // Number of samples for bias calibration
static constexpr float kImpactThresholdMps2 = 12.0f; // Rough threshold to log a punch (m/s^2)
static constexpr uint32_t kPrintIntervalMs = 20;     // ~50 Hz print rate

Adafruit_MPU6050 mpu;

// Bias offsets estimated during startup calibration
float ax_bias = 0.0f;
float ay_bias = 0.0f;
float az_bias = 0.0f;

float peak_magnitude_mps2 = 0.0f;
uint32_t last_print_ms = 0;

bool logging_enabled = false;

void calibrateSensor();
void printHeader();
void readAndReport();
void waitForLoggingChoice();

void waitForLoggingChoice() {
  Serial.println("Start logging to CSV? (Y/N)");
  const unsigned long start = millis();
  while (millis() - start < 10000) { // 10s timeout
    if (Serial.available()) {
      const char c = Serial.read();
      if (c == 'Y' || c == 'y') {
        logging_enabled = true;
      }
      break;
    }
    delay(10);
  }
  Serial.print("Logging ");
  Serial.println(logging_enabled ? "ENABLED" : "DISABLED");
}


void setup() {
    Serial.begin(kSerialBaud);
    while (!Serial) {
        delay(10);
    }

    if (!mpu.begin()) {
        Serial.println("MPU6050 not found. Check wiring and address (default 0x68).");
        while (true) {
            delay(1000);
        }
    }

    // Configure accelerometer to ±16g for higher headroom on impacts.
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    calibrateSensor();
    waitForLoggingChoice();
    if (logging_enabled) {
        printHeader();
    }
}


void loop() {
    readAndReport();
}

void calibrateSensor() {
    Serial.println("Calibrating accelerometer... Hold the target still.");

    float ax_sum = 0.0f;
    float ay_sum = 0.0f;
    float az_sum = 0.0f;

    for (size_t i = 0; i < kCalibrationSamples; ++i) {
        sensors_event_t accel, gyro, temp;
        mpu.getEvent(&accel, &gyro, &temp);
        ax_sum += accel.acceleration.x;
        ay_sum += accel.acceleration.y;
        az_sum += accel.acceleration.z - SENSORS_GRAVITY_STANDARD; // Remove gravity from Z
        delay(5);
    }

    ax_bias = ax_sum / static_cast<float>(kCalibrationSamples);
    ay_bias = ay_sum / static_cast<float>(kCalibrationSamples);
    az_bias = az_sum / static_cast<float>(kCalibrationSamples);

    Serial.print("Calibration complete. Bias (m/s^2): ");
    Serial.print(ax_bias, 4);
    Serial.print(", ");
    Serial.print(ay_bias, 4);
    Serial.print(", ");
    Serial.println(az_bias, 4);
}

void printHeader() {
    Serial.println("time_ms,ax_mps2,ay_mps2,az_mps2,net_mps2,peak_mps2,impact");
}

void readAndReport() {
    if (!logging_enabled) {
        return;
    }   

    const uint32_t now = millis();
    if (now - last_print_ms < kPrintIntervalMs) {
        return;
    }
    last_print_ms = now;

    sensors_event_t accel, gyro, temp;
    mpu.getEvent(&accel, &gyro, &temp);

    // Remove calibration bias; accel is already in m/s^2.
    const float ax = accel.acceleration.x - ax_bias;
    const float ay = accel.acceleration.y - ay_bias;
    const float az = accel.acceleration.z - az_bias;

    // Net acceleration magnitude (m/s^2)
    const float net_mps2 = sqrtf(ax * ax + ay * ay + az * az);

    // Track peaks to spot impacts.
    if (net_mps2 > peak_magnitude_mps2) {
        peak_magnitude_mps2 = net_mps2;
    }

    const bool impact = net_mps2 >= kImpactThresholdMps2;

    Serial.print(now);
    Serial.print(',');
    Serial.print(ax, 4);
    Serial.print(',');
    Serial.print(ay, 4);
    Serial.print(',');
    Serial.print(az, 4);
    Serial.print(',');
    Serial.print(net_mps2, 4);
    Serial.print(',');
    Serial.print(peak_magnitude_mps2, 4);
    Serial.print(',');
    Serial.println(impact ? "1" : "0");
}
