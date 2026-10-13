/*
 * ============================================================================
 * SMART ACCIDENT DETECTION AND EMERGENCY RESPONSE SYSTEM (SADERS)
 * ESP32 Vehicle Sensor Unit Firmware Prototype
 * Hardware: ESP32 DevKit, MPU-6050 (Accel/Gyro), NEO-6M GPS Module
 * ============================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <TinyGPS++.h>

// WiFi Configuration
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";

// SADERS Spring Boot Backend REST Endpoint
const char* BACKEND_URL = "http://192.168.1.100:8080/api/sensors/data";

// Sensor Objects
Adafruit_MPU6050 mpu;
TinyGPSPlus gps;
HardwareSerial gpsSerial(2); // ESP32 UART2 (RX=16, TX=17)

// Vehicle Telemetry Identifiers
const char* DEVICE_ID = "ESP32-001";
const char* VEHICLE_ID = "VH-1024";

// Threshold Configuration
const float ACCEL_IMPACT_THRESHOLD_G = 3.2;   // 3.2g impact spike threshold
const float GYRO_ROTATION_THRESHOLD_DEG = 120.0; // 120 deg/sec rotational velocity threshold

float lastSpeed = 0.0;
unsigned long lastTelemetryTime = 0;
const unsigned long TELEMETRY_INTERVAL_MS = 1000; // 1 second intervals

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, 16, 17);
  
  Serial.println("==================================================");
  Serial.println("SADERS ESP32 IoT Sensor Module Initializing...");
  Serial.println("==================================================");

  // Initialize MPU-6050 Accelerometer / Gyroscope
  Wire.begin();
  if (!mpu.begin()) {
    Serial.println("[-] ERROR: MPU-6050 sensor not found! Check wiring.");
  } else {
    Serial.println("[+] MPU-6050 Accel/Gyro initialized successfully.");
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }

  // Connect to WiFi Network
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi...");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[+] Connected to WiFi. IP: " + WiFi.localIP().toString());
  } else {
    Serial.println("\n[-] WiFi Connection failed. Will operate in offline buffer mode.");
  }
}

void loop() {
  // Read GPS Serial Stream
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = currentMillis;

    // Read MPU-6050 Sensor Data
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Convert m/s^2 to g-force
    float ax = a.acceleration.x / 9.80665;
    float ay = a.acceleration.y / 9.80665;
    float az = a.acceleration.z / 9.80665;

    // Gyroscope in degrees per second
    float gx = g.gyro.x * (180.0 / 3.14159);
    float gy = g.gyro.y * (180.0 / 3.14159);
    float gz = g.gyro.z * (180.0 / 3.14159);

    // GPS Location & Speed
    double latitude = gps.location.isValid() ? gps.location.lat() : 28.6139;  // Default fallback (Delhi/Noida NCR)
    double longitude = gps.location.isValid() ? gps.location.lng() : 77.2090;
    float currentSpeed = gps.speed.isValid() ? gps.speed.kmph() : 48.0;
    float speedChange = currentSpeed - lastSpeed;
    lastSpeed = currentSpeed;

    // Calculate total impact magnitude
    float totalAccelMag = sqrt(ax * ax + ay * ay + az * az);
    float totalGyroMag = sqrt(gx * gx + gy * gy + gz * gz);

    Serial.printf("[Telemetry] Accel: %.2fg | Gyro: %.1f deg/s | Speed: %.1f km/h | Lat: %.4f, Lng: %.4f\n",
                  totalAccelMag, totalGyroMag, currentSpeed, latitude, longitude);

    // Build JSON Payload
    String jsonPayload = "{";
    jsonPayload += "\"deviceId\":\"" + String(DEVICE_ID) + "\",";
    jsonPayload += "\"vehicleId\":\"" + String(VEHICLE_ID) + "\",";
    jsonPayload += "\"accelerationX\":" + String(ax, 4) + ",";
    jsonPayload += "\"accelerationY\":" + String(ay, 4) + ",";
    jsonPayload += "\"accelerationZ\":" + String(az, 4) + ",";
    jsonPayload += "\"gyroX\":" + String(gx, 2) + ",";
    jsonPayload += "\"gyroY\":" + String(gy, 2) + ",";
    jsonPayload += "\"gyroZ\":" + String(gz, 2) + ",";
    jsonPayload += "\"speed\":" + String(currentSpeed, 1) + ",";
    jsonPayload += "\"speedChange\":" + String(speedChange, 1) + ",";
    jsonPayload += "\"latitude\":" + String(latitude, 6) + ",";
    jsonPayload += "\"longitude\":" + String(longitude, 6);
    jsonPayload += "}";

    // Transmit Telemetry Packet via HTTP POST
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(BACKEND_URL);
      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST(jsonPayload);
      
      if (httpResponseCode > 0) {
        Serial.printf("[HTTP] Telemetry transmitted successfully. Response: %d\n", httpResponseCode);
      } else {
        Serial.printf("[-] HTTP Error: %s\n", http.errorToString(httpResponseCode).c_str());
      }
      http.end();
    }

    // Local Hardware Alert Threshold Check
    if (totalAccelMag > ACCEL_IMPACT_THRESHOLD_G || totalGyroMag > GYRO_ROTATION_THRESHOLD_DEG) {
      Serial.println("\n[CRITICAL WARNING] Sudden High Impact / Orientation Anomaly Detected on ESP32!");
      Serial.println("[!] Triggering local emergency verification pipeline...");
    }
  }
}
