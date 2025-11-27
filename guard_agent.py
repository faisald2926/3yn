import cv2
import os
import time
from ultralytics import YOLO
from datetime import datetime

# --- CONFIG ---
MODEL_PATH = './runs/detect/3yn_Ultimate_v32/weights/best.onnx' 
CAMERA_SOURCE = 0 
CONFIDENCE_HRESHOLD = 0.60
ALERT_FOLDER = "alerts"
ALERT_COOLDOWN = 1.0 

if not os.path.exists(ALERT_FOLDER): os.makedirs(ALERT_FOLDER)

print(f"Loading: {MODEL_PATH}")
model = YOLO(MODEL_PATH, task='detect')
cap = cv2.VideoCapture(CAMERA_SOURCE)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("3yn Active. Press 'q' to quit.")
last_alert_time = 0

while True:
    ret, frame = cap.read()
    if not ret: break

    # 1. Inference
    results = model.predict(frame, conf=CONFIDENCE_HRESHOLD, verbose=False)
    threat_detected = False
    
    # 2. Prepare Data
    clean_frame = frame.copy()      # For Training (No box)
    display_frame = frame.copy()    # For Dashboard (With box)
    
    detections_txt = []

    for r in results:
        # Draw boxes on display frame only
        display_frame = r.plot()
        
        if len(r.boxes) > 0:
            threat_detected = True
            for box in r.boxes:
                # Get Math for Training
                cls = int(box.cls[0])
                x, y, w, h = box.xywhn[0].tolist()
                detections_txt.append(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")

    # 3. Show Live Feed
    cv2.imshow("3yn Eye", display_frame)

    # 4. Save The "Triple Set"
    current_time = time.time()
    if threat_detected and (current_time - last_alert_time > ALERT_COOLDOWN):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base_name = f"alert_{timestamp}"
        
        # A. Save Display Image (For Human)
        cv2.imwrite(f"{ALERT_FOLDER}/{base_name}_display.jpg", display_frame)
        
        # B. Save Clean Image (For AI Training)
        cv2.imwrite(f"{ALERT_FOLDER}/{base_name}.jpg", clean_frame)
        
        # C. Save Label Text (For AI Training)
        with open(f"{ALERT_FOLDER}/{base_name}.txt", "w") as f:
            f.write("\n".join(detections_txt))
            
        print(f"Logged Threat: {base_name}")
        last_alert_time = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()