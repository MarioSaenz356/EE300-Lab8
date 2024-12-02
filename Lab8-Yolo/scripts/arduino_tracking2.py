from ultralytics import YOLO
import cv2
import serial
import time

# Initialize Arduino serial communication
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)  # Adjust 'COM5' to your Arduino's port
time.sleep(2)  # Allow time for the Arduino to reset

# Load the YOLOv8 model
model = YOLO("C:/Users/esteb/Documents/NMSU/CLASSES/FALL 2024/EE300/Lab8-Yolo/trained_model/nmsu_logo_detection4/weights/best.pt")

# Open the external camera and set resolution to 480p
cap = cv2.VideoCapture(1)  # Replace 1 with the external camera index
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Constants
DEADBAND = 15  # Deadband threshold in pixels
pan_angle = 90  # Initial pan angle
tilt_angle = 90  # Initial tilt angle

# Function to send servo commands to Arduino
def send_servo_command(pan, tilt):
    command = f"{pan},{tilt}\n"
    arduino.write(command.encode())

# Function to smooth servo movements
def smooth_servo_angle(current_angle, target_angle, step=1):
    if abs(current_angle - target_angle) <= step:
        return target_angle
    elif current_angle < target_angle:
        return current_angle + step
    else:
        return current_angle - step

# Function to calculate servo adjustments
def adjust_servo_angles(x_center, y_center, frame_width, frame_height, pan, tilt):
    # Calculate offsets from frame center
    x_offset = x_center - (frame_width // 2)
    y_offset = y_center - (frame_height // 2)

    # Apply deadband logic
    if abs(x_offset) <= DEADBAND:
        pan_adjust = 0  # No adjustment if within deadband
    else:
        pan_adjust = int(-x_offset / (frame_width / 90))  # Larger divisor for slower movement

    if abs(y_offset) <= DEADBAND:
        tilt_adjust = 0  # No adjustment if within deadband
    else:
        tilt_adjust = int(y_offset / (frame_height / 90))  # Larger divisor for slower movement

    # Update servo angles with smoothing
    pan = smooth_servo_angle(pan, pan + pan_adjust)
    tilt = smooth_servo_angle(tilt, tilt + tilt_adjust)

    return pan, tilt

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 detection
    results = model.predict(frame, conf=0.5)

    # Draw the detections
    annotated_frame = results[0].plot()

    # If detections are present
    if len(results[0].boxes) > 0:
        # Get the first detection
        box = results[0].boxes[0]
        x_center = int((box.xywh[0][0] + box.xywh[0][2]) / 2)
        y_center = int((box.xywh[0][1] + box.xywh[0][3]) / 2)

        # Adjust servo angles to center the logo
        pan_angle, tilt_angle = adjust_servo_angles(
            x_center, y_center, 640, 480, pan_angle, tilt_angle
        )

        # Send new angles to the Arduino
        send_servo_command(pan_angle, tilt_angle)

    # Display the frame
    cv2.imshow("Tracking", annotated_frame)

    # Break the loop on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
