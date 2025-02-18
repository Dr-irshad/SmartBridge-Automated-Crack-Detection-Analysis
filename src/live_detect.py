import os
import cv2
from ultralytics import YOLO
from ultralytics import settings

# Disable specific integrations
settings.comet = False
settings.mlflow = False
settings.tensorboard = False
settings.wandb = False

if __name__ == '__main__':
    # Load the trained YOLO model
    model = YOLO("best.pt")  # Ensure 'best.pt' is the trained model

    # Open webcam
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Run inference
        results = model(frame)
        
        # Display results
        for r in results:
            frame = r.plot()
        
        cv2.imshow("YOLOv8 Webcam Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

