import cv2
import numpy as np
from typing import List, Tuple, Dict, Any

class ObjectDetector:
    def __init__(self):
        self.model = None
        self.classes = []
        self.is_initialized = False

    def initialize_model(self, weights_path: str, config_path: str, classes_path: str) -> None:
        """Initialize YOLO model with given weights and configuration."""
        try:
            self.model = cv2.dnn.readNet(weights_path, config_path)
            with open(classes_path, 'r') as f:
                self.classes = f.read().splitlines()
            self.is_initialized = True
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.is_initialized = False

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess frame for YOLO model."""
        blob = cv2.dnn.blobFromImage(
            frame, 
            1/255.0,  # Scale factor
            (416, 416),  # Output size
            swapRB=True,
            crop=False
        )
        return blob

    def detect_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect objects in the given frame."""
        if not self.is_initialized:
            return []

        height, width = frame.shape[:2]
        blob = self.preprocess_frame(frame)
        
        # Run detection
        self.model.setInput(blob)
        output_layers = self.model.getUnconnectedOutLayersNames()
        layer_outputs = self.model.forward(output_layers)

        # Process outputs
        detections = []
        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > 0.5:  # Confidence threshold
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    
                    detections.append({
                        'class': self.classes[class_id],
                        'confidence': float(confidence),
                        'bbox': (x, y, w, h)
                    })

        return detections

    def annotate_frame(self, frame: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """Draw bounding boxes and labels on the frame."""
        annotated_frame = frame.copy()
        
        for detection in detections:
            x, y, w, h = detection['bbox']
            label = f"{detection['class']} {detection['confidence']:.2f}"
            
            # Draw rectangle and label
            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                annotated_frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )
            
        return annotated_frame

# Create a single instance to be used across the application
object_detector = ObjectDetector()
