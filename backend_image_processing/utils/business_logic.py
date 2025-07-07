"""
This module provides utility functions for processing and visualizing parking slot occupancy using OpenCV.
Functions:
    process_roi(dilated, roi, white_pixel_thresh_free, white_pixel_thresh_occupied, prev_state):
        Analyzes a region of interest (ROI) in a dilated image to determine if a parking slot is occupied or free,
        based on contour area thresholds. Returns the occupancy status and the total area of detected contours.
    draw_slot_status(frame, roi, white, occupied):
        Draws a rectangle and label on the frame to indicate the status (Occupied/Free) of a parking slot.
    vote_slot(history, history_size):
        Determines the majority occupancy status from a slot's history using a simple voting mechanism.
    update_slot_history(slot_history, idx, is_occupied):
        Updates the occupancy history for a specific slot index with the latest status.
    overlay_available_count(frame, available, total):
        Overlays the count of available parking slots on the frame.
"""

import cv2


def process_roi(dilated, roi, white_pixel_thresh_free, white_pixel_thresh_occupied, prev_state):
    x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]
    roi_crop = dilated[y:y + h, x:x + w]
    
    contours, _ = cv2.findContours(roi_crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    total_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        total_area += area
    
     
    
    total_area = int(total_area)
    
   
    white = cv2.countNonZero(roi_crop)
    
    combined_area = (white*2 + total_area) / 3  
    
    # I use this only for debugging purposes  
    # print(total_area , white , combined_area)
    

    
    if combined_area > white_pixel_thresh_occupied:
        is_occupied = True
    elif combined_area < white_pixel_thresh_free:
        is_occupied = False
    else:
        is_occupied = prev_state

    return is_occupied, combined_area


def draw_slot_status(frame, roi, white, occupied):
    x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]
    color = (0, 0, 255) if occupied else (0, 255, 0)
    label = "Occupied" if occupied else "Free"
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # cv2.putText(frame, f"{white}", (x + 5, y + h - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    # I use this only for debugging purposes

    cv2.putText(frame, label, (x, y - 8),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


def vote_slot(history, history_size):
    return sum(history) > (history_size // 2)

def update_slot_history(slot_history, idx, is_occupied):
    slot_history[idx].append(is_occupied)
    return slot_history[idx]

def overlay_available_count(frame, available, total):
    cv2.putText(frame, f"Available: {available}/{total}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)