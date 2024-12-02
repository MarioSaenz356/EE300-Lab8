#include <Servo.h>

Servo panServo;  // Servo for horizontal movement
Servo tiltServo; // Servo for vertical movement

int panPin = 2;   // Arduino pin for the pan servo
int tiltPin = 3; // Arduino pin for the tilt servo

void setup() {
    panServo.attach(panPin);
    tiltServo.attach(tiltPin);

    // Set initial position
    panServo.write(90);  // Center position
    tiltServo.write(90);

    Serial.begin(9600);  // Start serial communication
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');  // Read serial input
        int commaIndex = command.indexOf(',');

        if (commaIndex != -1) {
            int panAngle = command.substring(0, commaIndex).toInt();
            int tiltAngle = command.substring(commaIndex + 1).toInt();

            // Move servos to the received angles
            panServo.write(panAngle);
            tiltServo.write(tiltAngle);
        }
    }
}
