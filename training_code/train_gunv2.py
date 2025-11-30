from ultralytics import YOLO
import os
import torch

def main():
    # --- CONFIGURATION ---
    yaml_path = r"D:\WeaponsDetector\guns.v2i.yolov8\data.yaml"

    MODEL_NAME = 'yolov8s.pt'
    EPOCHS = 50
    IMG_SIZE = 640
    BATCH_SIZE = 16
    PROJECT_NAME = '3yn_Training_Run_Fixed' 

    # Check for GPU
    if torch.cuda.is_available():
        print(f"✅ 3yn is using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ WARNING: Using CPU. This will be slow.")

    # 1. LOAD MODEL
    print("\n[1/4] Initializing 3yn Brain...")
    model = YOLO(MODEL_NAME)

    # 2. TRAIN
    print(f"\n[2/4] Training 3yn on custom data...")
    # workers=0 fixes multiprocessing issues on Windows if the main block doesn't
    results = model.train(
        data=yaml_path,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        name=PROJECT_NAME,
        device=0,
        verbose=True,
        workers=0  
    )

    # 3. TEST AFTER
    print("\n[3/4] Validating 3yn Performance...")
    metrics_post = model.val(split='test', verbose=False)
    print(f"   >>> 3yn Final Accuracy (mAP50): {metrics_post.box.map50:.2%}")

    # 4. EXPORT
    print("\n[4/4] Exporting 3yn to ONNX...")
    path = model.export(format='onnx')
    print(f"✅ 3yn Ready! Model saved at: {path}")

if __name__ == '__main__':

    main()
