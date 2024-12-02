# Import necessary libraries
from ultralytics import YOLO
import cv2

# Load the trained YOLOv8 model
model = YOLO("C:/Users/esteb/Documents/NMSU/CLASSES/FALL 2024/EE300/Lab8-Yolo/trained_model/nmsu_logo_detection4/weights/best.pt")  # Replace with the path to your trained YOLOv8 model

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam; change if you have multiple cameras

# Check if the webcam is accessible
if not cap.isOpened():
    print("Error: Cannot access the webcam")
    exit()

# Loop to process the webcam feed
while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame from webcam")
        break

    # Run YOLOv8 detection on the frame
    results = model.predict(source=frame, conf=0.5)  # Adjust the confidence threshold as needed (default: 0.5)

    # Annotate the frame with bounding boxes and labels
    annotated_frame = results[0].plot()

    # Display the annotated frame in a window
    cv2.imshow("Object Detection", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
