import cv2
import json
import os

# === Load video and grab a reference frame ===
video_path = "../video/carPark.mp4"
cap = cv2.VideoCapture(video_path)

cap.set(cv2.CAP_PROP_POS_FRAMES, 50)  # Use a good middle frame
ret, frame = cap.read()
cap.release()

if not ret:
    raise Exception(" Failed to read video frame for ROI selection.")

# === ROI Selection ===
print(" Select parking slots (press ENTER when done)")
rois = cv2.selectROIs("Select Parking Slots", frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# === Save ROIs as JSON ===
roi_data = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for x, y, w, h in rois]
os.makedirs("data", exist_ok=True)

with open("data/rois.json", "w") as f:
    json.dump(roi_data, f, indent=4)

print(f" Saved {len(roi_data)} parking slots to data/rois.json")
