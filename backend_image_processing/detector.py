"""
This module provides functionality for detecting parking slot occupancy in video frames.
Imports:
    - cv2: OpenCV library for image and video processing.
    - deque: Double-ended queue for maintaining slot status history.
    - time: For frame rate control.
    - backend_image_processing.utils.load: Module for loading resources.
    - backend_image_processing.utils.image_preprocess: Module for frame preprocessing and slot detection.
    - backend_image_processing.utils.draw_overlays: Module for drawing overlays on frames.
    - backend_image_processing.utils.encoder: Module for encoding frames for output.
Functions:
    generate_detected_frames(
        video_path="./video/carPark.mp4",
        roi_file="data/rois.json",
        history_size=5
    ):
        Generator function that yields video frames with detected parking slot statuses.
        Args:
            video_path (str): Path to the input video file.
            roi_file (str): Path to the JSON file containing regions of interest (ROIs) for parking slots.
            white_pixel_thresh_free (int): Threshold of white pixels to consider a slot as free.
            white_pixel_thresh_occupied (int): Threshold of white pixels to consider a slot as occupied.
            history_size (int): Number of previous frames to consider for slot status smoothing.
        Yields:
            bytes: Encoded video frame with overlays indicating parking slot statuses.
        Side Effects:
            - Reads frames from the video file.
            - Draws overlays on frames to indicate slot statuses.
            - Sleeps to maintain a frame rate of approximately 30 FPS.
            - Releases the video capture resource when done.
"""

import cv2
from collections import deque
import time

# === Utility Functions for Parking Slot Detection ===

import backend_image_processing.utils.load as load_module
import backend_image_processing.utils.image_preprocess as image_preprocess_module
import backend_image_processing.utils.draw_overlays as draw_overlays_module
import backend_image_processing.utils.encoder as encoder_module


# === Generator Function to Yield Video Frames ===
def generate_detected_frames(video_path="./video/carPark.mp4", 
                             roi_file="data/rois.json" ,
                             white_pixel_thresh_free=800,
                             white_pixel_thresh_occupied=1000,
                             history_size=5):
    

    roi_data, cap = load_module.load_resources(video_path, roi_file)

    slot_history = [deque(maxlen=history_size) for _ in roi_data]
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, frame = cap.read()
        if not success:
            break
      
        available, slot_statuses = image_preprocess_module.process_frame(
            frame, roi_data, slot_history, white_pixel_thresh_free, white_pixel_thresh_occupied, history_size)

        draw_overlays_module.draw_overlays(frame, slot_statuses, available, len(roi_data))
    
        yield encoder_module.encode_frame(frame)
        time.sleep(1 / 30.0)

    cap.release()
