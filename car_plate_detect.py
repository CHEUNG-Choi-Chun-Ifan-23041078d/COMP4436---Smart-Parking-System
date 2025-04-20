import cv2
import numpy as np
from ultralytics import YOLO
import pytesseract
import time

MODEL_PATH = "/Users/ifancheung/Desktop/IoT Parking/Car Plate detect/license_plate_detector.pt"

model = YOLO(MODEL_PATH)
print(f"Loaded YOLO model from {MODEL_PATH}")

def preprocess_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.fastNlMeansDenoising(thresh)
    resized = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return resized

def ocr_plate(plate_image):
    processed = preprocess_for_ocr(plate_image)
    config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed, config=config).strip()
    text = ''.join(c for c in text if c.isalnum()).upper()
    return text if text else "Unknown"

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Starting webcam feed. Press 'q' to quit.")

while True:
    try:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        results = model(frame)
        
        detected = False
        plate_text = "No Plate"
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            
            for box, conf in zip(boxes, confidences):
                if conf < 0.5: 
                    continue
                
                detected = True
                x1, y1, x2, y2 = map(int, box)
                
                plate_region = frame[y1:y2, x1:x2]
                
                plate_text = ocr_plate(plate_region)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                text = f"{plate_text} ({conf:.2f})"
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                text_bg = (x1, y1 - text_height - 10)
                cv2.rectangle(frame, 
                            (x1, y1 - text_height - 10),
                            (x1 + text_width, y1),
                            (0, 255, 0),
                            -1)
                
                cv2.putText(frame, text,
                           (x1, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                           (0, 0, 0), 2)
        
        processing_time = time.time() - start_time
        
        plate_display = f"Plate: {plate_text}"
        time_display = f"Time: {processing_time:.2f}s"
        
        (plate_width, plate_height), _ = cv2.getTextSize(plate_display, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.rectangle(frame, (10, 10), (10 + plate_width, 10 + plate_height + 10), (0, 0, 0), -1)
        cv2.putText(frame, plate_display, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        (time_width, time_height), _ = cv2.getTextSize(time_display, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        cv2.rectangle(frame, (10, 40), (10 + time_width, 40 + time_height + 10), (0, 0, 0), -1)
        cv2.putText(frame, time_display, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        if detected:
            print(f"Detected Plate: {plate_text}")
            print(f"Processing Time: {processing_time:.2f} seconds")

        cv2.imshow("License Plate Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    except Exception as e:
        print(f"Error processing frame: {str(e)}")
        continue

cap.release()
cv2.destroyAllWindows()
print("Webcam feed stopped.")