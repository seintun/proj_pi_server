"""
Object Detection Package

This package provides YOLO-based object detection functionality for the Raspberry Pi server.

To use this package:
1. Download YOLO weights file (e.g., yolov3.weights)
2. Download YOLO configuration file (e.g., yolov3.cfg)
3. Create a classes file (e.g., coco.names) containing class names, one per line

Example usage:
    from object_detection.detector import object_detector
    
    # Initialize the detector
    object_detector.initialize_model(
        weights_path='path/to/yolov3.weights',
        config_path='path/to/yolov3.cfg',
        classes_path='path/to/coco.names'
    )
    
    # Use in video processing
    frame = camera.read()
    detections = object_detector.detect_objects(frame)
    annotated_frame = object_detector.annotate_frame(frame, detections)
"""

from .detector import ObjectDetector, object_detector

__all__ = ['ObjectDetector', 'object_detector']
