"""
Utility functions for loading video resources and region of interest (ROI) data.
Functions:
    load_resources(video_path, roi_file):
        Loads ROI data from a JSON file and opens a video file for processing.
        Args:
            video_path (str): Path to the video file.
            roi_file (str): Path to the ROI JSON file.
        Returns:
            tuple: (roi_data (dict), cap (cv2.VideoCapture)).
    load_rois(roi_file):
        Loads ROI data from a JSON file.
        Args:
            roi_file (str): Path to the ROI JSON file.
        Returns:
            dict: ROI data loaded from the file.
    load_video(video_path):
        Opens a video file for processing using OpenCV.
        Args:
            video_path (str): Path to the video file.
        Returns:
            cv2.VideoCapture: Video capture object.
        Raises:
            Exception: If the video file cannot be opened.
"""


import json
import cv2

def load_resources(video_path, roi_file):
        roi_data = load_rois(roi_file)
        cap = load_video(video_path)
        return roi_data, cap


def load_rois(roi_file):
    with open(roi_file, "r") as f:
        return json.load(f)\
        

def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Cannot open video.")
    return cap

