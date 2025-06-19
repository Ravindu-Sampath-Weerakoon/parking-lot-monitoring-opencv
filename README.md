# 🚗 Smart Parking Slot Detection System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey?logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-green?logo=opencv)
![License](https://img.shields.io/badge/License-Educational-lightblue)

---

> **A real-time web application for detecting available and occupied parking slots using computer vision.**

---

## 📸 Demo

![Parking Demo](https://user-images.githubusercontent.com/placeholder/demo.gif)
<sup><em>(Replace with your own demo GIF or screenshot)</em></sup>

---

## 🗂️ Project Structure

```plaintext
parking_project/
│
├── app.py                      # Flask web server
├── environment.yml             # Conda environment setup
├── backend_image_processing/
│   ├── detector.py             # Main detection pipeline
│   ├── calibrate.py            # ROI calibration tool
│   └── utils/                  # Helper modules
│       ├── business_logic.py
│       ├── draw_overlays.py
│       ├── encoder.py
│       ├── image_preprocess.py
│       └── load.py
├── data/
│   └── rois.json               # Parking slot ROI data
├── video/
│   └── carPark.mp4             # Sample parking lot video
├── templates/
│   └── index.html              # Web interface
└── static/
    └── style.css               # App styling
```

---

## 🛠️ Features

- **Real-Time Detection:** Instantly shows free and occupied slots.
- **Web Interface:** Clean, responsive UI for live monitoring.
- **Easy Calibration:** Select parking slots visually and save as JSON.
- **Modular Design:** Easily extend or modify detection logic.

---

## 🚀 Quick Start

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd parking_project
conda env create -f environment.yml
conda activate parking_env
```

### 2. Calibrate Parking Slots

```bash
python backend_image_processing/calibrate.py
```
_Select parking slots on the video frame. Data is saved to `data/rois.json`._

### 3. Run the Web App

```bash
python app.py
```
Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## 🖼️ How It Works

1. **Calibration:**  
   Select parking slot regions on a sample video frame.
2. **Detection:**  
   Each frame is preprocessed and analyzed to determine slot status.
3. **Visualization:**  
   Results are overlaid and streamed to the web interface.



---

## ⚙️ Customization

- **Change Video:** Replace `video/carPark.mp4` with your own footage.
- **Recalibrate:** Rerun the calibration script for new layouts.

---

## 📦 Requirements

- Python 3.10+
- OpenCV
- Flask
- Numpy
- (See `environment.yml` for full list)

---

## ✨ Credits

Designed by Ravindu Weerakoon  
For educational use.

---

## 📄 License

This project is for educational purposes.
