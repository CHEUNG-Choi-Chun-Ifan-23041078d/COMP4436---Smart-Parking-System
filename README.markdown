# Smart Parking System

This document provides instructions for accessing and running the Car Plate Detection project, which includes an ESP32S module, a Python-based license plate detection script using a YOLO model, and a web dashboard for visualization.

## Project Overview

The Car Plate Detection project enables real-time license plate detection using a trained YOLO model, integrates with an ESP32S module for IoT functionality, and provides a web dashboard to monitor results. Follow the steps below to set up and run the project components.

## Prerequisites

Before proceeding, ensure you have the following:

- **Hardware**:
  - ESP32S module
  - Webcam (for Python script, if using real-time detection)
- **Software**:
  - [Arduino IDE](https://www.arduino.cc/en/software) for ESP32S programming
  - Python 3.8+ with required libraries (see Python section)
  - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
  - Web browser (e.g., Chrome, Firefox) for the dashboard
- **Files**:
  - `ESP32S.txt`: ESP32S code
  - `car_plate_detect.py`: Python script for plate detection
  - `license_plate_detector.pt`: YOLO model for plate detection
  - `Dashboard.zip`: Web dashboard source code

## Setup Instructions

### 1. ESP32S Module

The ESP32S module handles IoT-related tasks for the project. The provided code is in `ESP32S.txt` and must be converted to an Arduino-compatible format.

#### Steps:
1. **Rename the File**:
   - Locate `ESP32S.txt` in the project directory.
   - Rename it to `ESP32S.ino` to make it compatible with the Arduino IDE.
     ```bash
     mv ESP32S.txt ESP32S.ino
     ```
2. **Open in Arduino IDE**:
   - Launch the Arduino IDE.
   - Open `ESP32S.ino` via `File > Open`.
3. **Configure and Upload**:
   - Connect the ESP32S module to your computer via USB.
   - Select the board: `Tools > Board > ESP32 > ESP32 Dev Module`.
   - Select the port: `Tools > Port`.
   - Upload the code: Click the `Upload` button or press `Ctrl+U`.
4. **Verify**:
   - Open the Serial Monitor (`Tools > Serial Monitor`, 115200 baud) to confirm the ESP32S is running correctly.

### 2. Python Script for Car Plate Detection

The Python script `car_plate_detect.py` uses the YOLO model `license_plate_detector.pt` to detect license plates in images or webcam feeds, extracting text via OCR.

#### Requirements:
- Install dependencies:
  ```bash
  pip install ultralytics pytesseract opencv-python pillow
  ```
- Install Tesseract OCR:
  - On macOS:
    ```bash
    brew install tesseract
    ```
  - Verify:
    ```bash
    tesseract --version
    ```
- Ensure the YOLO model is at:
  ```
  /path/to/project/license_plate_detector.pt
  ```

#### Running the Script:
1. **Verify Paths**:
   - Ensure `car_plate_detect.py` and `license_plate_detector.pt` are in the project directory.
   - Update the script’s model path if necessary (default assumes local directory).
2. **Run the Script**:
   - For webcam detection:
     ```bash
     python car_plate_detect.py
     ```
   - For image-based detection (if script supports it), specify an image directory:
     ```bash
     python car_plate_detect.py --input /path/to/images
     ```
3. **Expected Output**:
   - A window displays the video feed or image with detected plates, bounding boxes, and OCR text.
   - Console outputs the detected plate text (e.g., `WP969`) and processing time.
   - Press 'q' to exit webcam mode (if applicable).

#### Troubleshooting:
- **Webcam Issues**:
  - If the webcam fails, try a different index (e.g., `cv2.VideoCapture(1)`).
  - Check permissions:
    ```bash
    tccutil reset Camera
    ```
- **Model Errors**:
  - Verify `license_plate_detector.pt` exists and is YOLOv8-compatible.
- **OCR Failures**:
  - Ensure Tesseract is installed and test OCR:
    ```python
    import pytesseract
    print(pytesseract.image_to_string('test.png'))
    ```

### 3. Web Dashboard

The web dashboard visualizes license plate detection results and is accessible online or via local deployment.

#### Accessing the Online Dashboard:
- Visit: [https://comp4436.snap-live.com](https://comp4436.snap-live.com)
- Requirements: Modern web browser (Chrome, Firefox, Safari).
- Note: Ensure an active internet connection.

#### Running Locally:
1. **Unzip the Dashboard**:
   - Locate `Dashboard.zip` in the project directory.
   - Unzip to access the full source code:
     ```bash
     unzip Dashboard.zip -d Dashboard
     ```
2. **View Source Code**:
   - Navigate to the `Dashboard` directory to explore HTML, CSS, JavaScript, and other files.
3. **Host Locally**:
   - Use a local server (e.g., Python’s HTTP server):
     ```bash
     cd Dashboard
     python -m http.server 8000
     ```
   - Open `http://localhost:8000` in a browser.
4. **Functionality**:
   - Displays detected license plates, timestamps, and other IoT data from the ESP32S.
   - Interactive interface for monitoring and analysis.

#### Troubleshooting:
- **Server Issues**:
  - Ensure port 8000 is free or use a different port:
    ```bash
    python -m http.server 8080
    ```
- **File Errors**:
  - Verify `Dashboard.zip` unzipped correctly:
    ```bash
    ls Dashboard
    ```

## Additional Notes

- **Project Directory**:
  - Ensure all files (`ESP32S.ino`, `car_plate_detect.py`, `license_plate_detector.pt`, `Dashboard.zip`) are in the same directory or update paths accordingly.
- **Testing**:
  - Test the ESP32S module independently to confirm IoT functionality.
  - Use a printed license plate (e.g., `WP969.png`) for webcam testing.
- **Support**:
  - For issues, check console outputs or browser developer tools (F12).
  - Contact the project maintainer with detailed error logs.

## License

This project is for educational purposes. Ensure compliance with local regulations for license plate detection and IoT deployments.

---

*Last Updated: April 20, 2025*
