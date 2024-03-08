//#include <Adafruit_MotorShield.h>
//#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Create motor objects
Adafruit_DCMotor *motor1 = AFMS.getMotor(1);
Adafruit_DCMotor *motor2 = AFMS.getMotor(2);

// IR sensor pins
#define LEFT_SENSOR_PIN A0
#define RIGHT_SENSOR_PIN A1

// Threshold for sensor readings
#define SENSOR_THRESHOLD 500

// Define motor speeds
#define MOTOR_SPEED 150

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize motor shield
  AFMS.begin();

  // Set motor speeds
  motor1->setSpeed(MOTOR_SPEED);
  motor2->setSpeed(MOTOR_SPEED);
}

void loop() {
  // Read sensor values
  int leftSensorValue = analogRead(LEFT_SENSOR_PIN);
  int rightSensorValue = analogRead(RIGHT_SENSOR_PIN);

  // Check left sensor
  if (leftSensorValue > SENSOR_THRESHOLD && rightSensorValue > SENSOR_THRESHOLD) {
    // Both sensors are off the line, stop motors
    motor1->run(RELEASE);
    motor2->run(RELEASE);
  } 
  else if (leftSensorValue > SENSOR_THRESHOLD) {
    // Turn left
    motor1->run(FORWARD);
    motor2->run(BACKWARD);
  } 
  else if (rightSensorValue > SENSOR_THRESHOLD) {
    // Turn right
    motor1->run(BACKWARD);
    motor2->run(FORWARD);
  } 
  else {
    // Move forward
    motor1->run(FORWARD);
    motor2->run(FORWARD);
  }

  // Print sensor values for debugging
  Serial.print("Left Sensor: ");
  Serial.print(leftSensorValue);
  Serial.print(" - Right Sensor: ");
  Serial.println(rightSensorValue);

  // Delay for stability
  delay(50);
}
