import cv2
from collections import deque
import time
import matplotlib.pyplot as plt

# === Utility Functions for Parking Slot Detection ===
import backend_image_processing.utils.load as load_module
import backend_image_processing.utils.image_preprocess as image_preprocess_module
import backend_image_processing.utils.draw_overlays as draw_overlays_module
import backend_image_processing.utils.encoder as encoder_module

def generate_detected_frames(
    video_path="./video/carPark.mp4", 
    roi_file="data/rois.json",
    white_pixel_thresh_free=800,
    white_pixel_thresh_occupied=1000,
    history_size=5,
    plot_processing_time=True
):
    roi_data, cap = load_module.load_resources(video_path, roi_file)
    slot_history = [deque(maxlen=history_size) for _ in roi_data]
    
    processing_times = []
    frame_numbers = []
    start_processing_time = time.time()  # Track when processing starts
    
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        success, frame = cap.read()
        if not success:
            break
        
        frame_start_time = time.time()
        available, slot_statuses = image_preprocess_module.process_frame(
            frame, roi_data, slot_history, white_pixel_thresh_free, white_pixel_thresh_occupied, history_size
        )
        frame_end_time = time.time()
        
        processing_time = (frame_end_time - frame_start_time) * 1000  # ms
        processing_times.append(processing_time)
        frame_numbers.append(len(processing_times))
        
        print(f"Frame {len(frame_numbers)}: {processing_time:.2f} ms")
        
        draw_overlays_module.draw_overlays(frame, slot_statuses, available, len(roi_data))
        yield encoder_module.encode_frame(frame)
        
        # Save plot after 1 second (only once)
        current_time = time.time()
        if plot_processing_time and (current_time - start_processing_time) >= 20.0 and len(processing_times) > 0:
            plt.figure(figsize=(10, 5))
            plt.plot(frame_numbers, processing_times, label="Processing Time (ms)", color='blue')
            plt.xlabel("Frame Number")
            plt.ylabel("Processing Time (ms)")
            plt.title("Frame Processing Time (First 20 Seconds)")
            plt.grid(True)
            plt.legend()
            plt.savefig("processing_time_firsts20_second.png")  # Save plot
            plt.close()  # Free memory
            plot_processing_time = False  # Ensure it runs only once
        
        time.sleep(1 / 30.0)  # Maintain ~30 FPS
    
    cap.release()