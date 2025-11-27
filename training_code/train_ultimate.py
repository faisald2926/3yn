from ultralytics import YOLO
import os
import torch

def main():
    # --- CONFIGURATION ---
    # 1. The Data
    YAML_PATH = r"D:\Downloads_HDD\WeaponsDetector\Guns and knives.v1i.yolov8\data.yaml"
    
    # 2. The Brain to Start From (THE OLDE 3yn_Training_Run_Fixed MODEL)
    START_MODEL = r"D:\Downloads_HDD\WeaponsDetector\3yn_WeaponsDetector\runs\detect\3yn_Training_Run_Fixed\weights\best.pt"

    PROJECT_NAME = '3yn_Ultimate_v3'
    EPOCHS = 50
    IMG_SIZE = 640
    BATCH_SIZE = 16

    # Check GPU
    if torch.cuda.is_available():
        print(f"✅ GPU Active: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ WARNING: CPU Mode")

    # --- 1. LOAD ---
    print(f"\n[1/6] Loading Core Brain: {START_MODEL}")
    model = YOLO(START_MODEL)

    # --- 2. PRE-TEST (BENCHMARK) ---
    print("\n[2/6] Testing Current Accuracy on New Data...")
    try:
        metrics_pre = model.val(data=YAML_PATH, split='test', verbose=False)
        score_pre = metrics_pre.box.map50
        print(f"   >>> STARTING ACCURACY: {score_pre:.2%}")
    except:
        print("   >>> Pre-test skipped (Classes might differ). Starting training anyway.")
        score_pre = 0.0

    # --- 3. TRAIN ---
    print(f"\n[3/6] Fine-Tuning on 4,000 Images...")
    results = model.train(
        data=YAML_PATH,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        name=PROJECT_NAME,
        device=0,
        workers=0, # Fix for Windows
        verbose=True
    )

    # --- 4. POST-TEST ---
    print("\n[4/6] Verifying New Intelligence...")
    metrics_post = model.val(split='test', verbose=False)
    score_post = metrics_post.box.map50

    # --- 5. REPORT ---
    print("\n" + "="*40)
    print("   3yn EVOLUTION REPORT")
    print("="*40)
    print(f"   Old Brain:   {score_pre:.2%}")
    print(f"   New Brain:   {score_post:.2%}")
    print(f"   IMPROVEMENT: +{score_post - score_pre:.2%}")
    print("="*40)

    # --- 6. EXPORT ---
    print("\n[6/6] Exporting to ONNX...")
    path = model.export(format='onnx')
    print(f"✅ DONE! Final file: {path}")

if __name__ == '__main__':
    main()