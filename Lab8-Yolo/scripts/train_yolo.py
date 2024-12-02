from ultralytics import YOLO
import os

# Verify dataset paths
print("Verifying dataset paths...")
paths = ["./dataset/train/images", "./dataset/val/images"]
for path in paths:
    if os.path.exists(path):
        print(f"Path exists: {path}")
    else:
        print(f"Path not found: {path}")
        exit(1)  # Exit the script if any path is missing

# Load the YOLOv8 model (using the pretrained "nano" version for speed)
model = YOLO("yolov8n.pt")

# Train the model
print("Starting training...")
model.train(
    data="./data.yaml",            # Path to the data.yaml file
    epochs=50,                     # Number of training epochs
    imgsz=640,                     # Image size for training
    batch=16,                      # Batch size
    project="./trained_model",     # Where to save training results
    name="nmsu_logo_detection",    # Subfolder inside the project folder for this specific run
    pretrained=True                # Use pretrained weights
)

# Print success message
print("Training completed!")

