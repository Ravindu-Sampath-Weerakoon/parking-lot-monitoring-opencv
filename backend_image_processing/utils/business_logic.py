import cv2


def process_roi(dilated, roi, white_pixel_thresh_free, white_pixel_thresh_occupied, prev_state):
    x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]
    roi_crop = dilated[y:y + h, x:x + w]
    white = cv2.countNonZero(roi_crop)
    if white > white_pixel_thresh_occupied:
        is_occupied = True
    elif white < white_pixel_thresh_free:
        is_occupied = False
    else:
        is_occupied = prev_state
    return is_occupied, white


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