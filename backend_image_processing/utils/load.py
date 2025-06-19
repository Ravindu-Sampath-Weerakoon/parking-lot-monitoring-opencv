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