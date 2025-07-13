
import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import os
import sys

# --- Setup Paths and Add Project Root to Sys.Path ---
def setup_paths():
    """Adds the parent directory to sys.path to allow for module imports."""
    # This makes the script runnable from the 'visualizations' directory
    # and allows it to find the 'backend_image_processing' module.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.append(project_root)

setup_paths()

# --- Import Project-Specific Modules ---
from backend_image_processing.utils.image_preprocess import preprocess_frame
from backend_image_processing.utils.business_logic import process_roi

# --- Constants ---
VIDEO_PATH = "../video/carPark.mp4"
ROI_PATH = "../data/rois.json"
OUTPUT_DIR = "visualizations/output"

# --- Main Functions ---
def extract_key_frames(video_path):
    """Extracts frames from the beginning, middle, and end of a video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}")
        return {}

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    positions = {
        "Beginning": 50,
        "Middle": total_frames // 2,
        "End": total_frames - 150 # A bit earlier from the very end
    }
    
    frames = {}
    for name, pos in positions.items():
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        success, frame = cap.read()
        if success:
            # Convert to RGB for matplotlib plotting
            frames[name] = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    cap.release()
    return frames

def visualize_and_save_pipeline(frame, frame_title):
    """Applies and visualizes the full preprocessing pipeline on a given frame and saves it."""
    print(f"Processing pipeline for {frame_title} frame...")

    # --- Apply each step of the pipeline ---
    original = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    median = cv2.medianBlur(thresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(median, kernel, iterations=1)
    
    stages = {
        '1. Original RGB Frame': original,
        '2. Grayscale': gray,
        '3. Gaussian Blur': blur,
        '4. Adaptive Threshold': thresh,
        '5. Median Blur': median,
        '6. Final Dilated Image': dilated
    }
    
    # --- Create Subplots ---
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))
    fig.suptitle(f'Image Processing Pipeline for {frame_title} Frame', fontsize=16)
    axes = axes.flatten()
    
    for i, (title, img) in enumerate(stages.items()):
        ax = axes[i]
        if len(img.shape) == 2:  # Grayscale image
            ax.imshow(img, cmap='gray')
        else:  # RGB image
            ax.imshow(img)
        ax.set_title(title)
        ax.axis('off')
            
    # plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.tight_layout()
    
    # --- Save the Figure ---
    output_path = os.path.join(OUTPUT_DIR, f"pipeline_{frame_title.lower()}.png")
    plt.savefig(output_path)
    print(f"Saved pipeline visualization to {output_path}")
    plt.close(fig) # Close the figure to free memory

    return dilated

def visualize_and_save_detection(original_frame, processed_frame, rois):
    """Visualizes the final detection boxes on a frame and saves it."""
    print("Processing final detection visualization...")
    output_frame = original_frame.copy()
    available = 0
    total_slots = len(rois)

    for roi in rois:
        # Assume a neutral previous state for this single-frame demonstration
        is_occupied, _ = process_roi(processed_frame, roi, 800, 1000, prev_state=False)
        
        # Draw the rectangle on the output frame
        x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
        color = (255, 0, 0) if is_occupied else (0, 255, 0)  # Red for occupied, Green for free
        cv2.rectangle(output_frame, (x, y), (x + w, y + h), color, 2)
        if not is_occupied:
            available += 1

    # Draw the available count
    cv2.putText(output_frame, f"Available: {available}/{total_slots}", (30, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

    # --- Create and Save Figure ---
    plt.figure(figsize=(15, 8))
    plt.imshow(output_frame)
    plt.title('Final Detection Result on Middle Frame')
    plt.axis('off')
    
    output_path = os.path.join(OUTPUT_DIR, "final_detection_result.png")
    plt.savefig(output_path)
    print(f"Saved final detection visualization to {output_path}")
    plt.close()

def visualize_and_save_roi_analysis(original_frame, processed_frame, rois):
    """Selects an occupied and a free ROI to visualize the core detection logic."""
    print("Processing ROI analysis visualization...")

    # --- Find one occupied and one free slot for demonstration ---
    occupied_roi_to_show = None
    free_roi_to_show = None
    
    for r in rois:
        is_occupied, _ = process_roi(processed_frame, r, 800, 1000, prev_state=False)
        if is_occupied and occupied_roi_to_show is None:
            occupied_roi_to_show = r
        elif not is_occupied and free_roi_to_show is None:
            free_roi_to_show = r
        if occupied_roi_to_show and free_roi_to_show:
            break
            
    rois_to_visualize = {
        "Occupied Slot": occupied_roi_to_show,
        "Free Slot": free_roi_to_show
    }

    for title, roi in rois_to_visualize.items():
        if roi is None:
            print(f"Could not find a sample '{title}' to visualize. Skipping.")
            continue

        # --- Extract ROI crops ---
        x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
        original_crop = original_frame[y:y+h, x:x+w]
        processed_crop = processed_frame[y:y+h, x:x+w]

        # --- Re-run detection to get metrics ---
        contours, _ = cv2.findContours(processed_crop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total_area = int(sum(cv2.contourArea(cnt) for cnt in contours))
        white_pixel_count = cv2.countNonZero(processed_crop)
        
        # --- Draw contours on a new image for visualization ---
        contour_img = cv2.cvtColor(processed_crop, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 1)

        # --- Create Subplots ---
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f'Detailed Analysis of an {title}', fontsize=16)

        # Plot 1: Original ROI
        axes[0].imshow(original_crop)
        axes[0].set_title('1. Original ROI')
        axes[0].axis('off')

        # Plot 2: Processed ROI
        axes[1].imshow(processed_crop, cmap='gray')
        axes[1].set_title('2. Processed (Dilated) ROI')
        axes[1].axis('off')

        # Plot 3: Contours and Metrics
        axes[2].imshow(contour_img)
        axes[2].set_title('3. Contours Found')
        axes[2].axis('off')
        
        # Add text with metrics
        text = f"White Pixels: {white_pixel_count}\nContour Area: {total_area}"
        fig.text(0.5, 0.05, text, ha='center', fontsize=12, wrap=True)

        # plt.tight_layout(rect=[0, 0.1, 1, 0.95])
        plt.tight_layout()
        
        # --- Save the Figure ---
        output_path = os.path.join(OUTPUT_DIR, f"roi_analysis_{title.lower().replace(' ', '_')}.png")
        plt.savefig(output_path)
        print(f"Saved ROI analysis to {output_path}")
        plt.close(fig)

# --- Main Execution Block ---
if __name__ == "__main__":
    print("--- Starting Methodology Visualization Script ---")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Extract key frames from the video
    key_frames = extract_key_frames(VIDEO_PATH)
    
    if key_frames:
        processed_frames = {}
        # 2. Process and visualize the pipeline for each frame
        for name, frame in key_frames.items():
            processed_frames[name] = visualize_and_save_pipeline(frame, name)
        
        # 3. Load ROI data
        with open(ROI_PATH, 'r') as f:
            roi_data = json.load(f)
        
        # 4. Visualize the final detection on the middle frame
        visualize_and_save_detection(
            original_frame=key_frames['Middle'],
            processed_frame=processed_frames['Middle'],
            rois=roi_data
        )

        # 5. Visualize the detailed ROI analysis
        visualize_and_save_roi_analysis(
            original_frame=key_frames['Middle'],
            processed_frame=processed_frames['Middle'],
            rois=roi_data
        )

    print("--- Script Finished ---")
