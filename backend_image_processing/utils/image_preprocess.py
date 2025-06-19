import cv2
import numpy as np

# === Utility Functions for business_logic in Parking Slot Detection ===
import backend_image_processing.utils.business_logic as business_logic_module

def process_frame(frame, roi_data, slot_history, white_pixel_thresh_free, white_pixel_thresh_occupied, history_size):
        dilated = preprocess_frame(frame)
        available = 0
        slot_statuses = []
        for idx, roi in enumerate(roi_data):
            prev_state = slot_history[idx][-1] if slot_history[idx] else False
            is_occupied, white = business_logic_module.process_roi(
                dilated, roi, white_pixel_thresh_free, white_pixel_thresh_occupied, prev_state)
            history = business_logic_module.update_slot_history(slot_history, idx, is_occupied)
            occupied = business_logic_module.vote_slot(history, history_size)
            if not occupied:
                available += 1
            slot_statuses.append((roi, white, occupied))
        return available, slot_statuses


def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(median, kernel, iterations=1)
    return dilated