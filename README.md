#  3yn (Ein): Autonomous Weapon Detection & Response System

**An intelligent, privacy-first security agent that detects weapons in real-time and evolves through human feedback.**

---

## 📖 Overview

Traditional CCTV systems are passive—they record crimes but don't stop them. **3yn** (Arabic for "Eye") transforms standard cameras into active guardians.

Using a custom fine-tuned **YOLOv8** model, 3yn monitors video feeds for firearms and knives. When a threat is detected, it instantly alerts security personnel via a centralized dashboard. The system features a unique **"Human-in-the-loop"** verification step: every time a guard confirms or dismisses an alert, the AI learns from that feedback, constantly reducing false alarms and adapting to its specific environment.

---

## 🚀 Key Features

- **YOLOv8 Intelligence:** Built on the state-of-the-art YOLOv8 architecture, optimized for speed and accuracy.
- **Massive Accuracy Gain:** Through rigorous **Transfer Learning**, we improved the model's Mean Average Precision (mAP50) from a baseline of **2.03%** to **92.25%** on our custom test set.
- **Active Learning Loop:** The system doesn't just detect; it learns. Dismissed alerts are automatically tagged as "False Positives" and used to retrain the model, solving the "Black Phone vs. Gun" problem.
- **Edge-First Privacy:** Video processing happens locally (using ONNX runtime), ensuring sensitive footage never leaves the premises unless a threat is verified.
- **Real-Time Command Center:** A professional **Streamlit** dashboard allows security teams to monitor multiple feeds and verify threats in milliseconds.

---

## 📊 Datasets & Training

Our model was trained and fine-tuned using a curated mix of open-source datasets to ensure robust detection of both handguns and knives:

1.  **Weapon Detection (Roboflow):** [Link](https://universe.roboflow.com/joao-assalim-xmovq/weapon-2/dataset/2)
2.  **Hit Product Weapon:** [Link](https://universe.roboflow.com/hit-product/weapon-detection-c9jaq)
3.  **Guns Dataset:** [Link](https://universe.roboflow.com/detection-xflrf/guns-zw6a4/dataset/2)
4.  **Guns and Knives:** [Link](https://universe.roboflow.com/luciferclarke001-gmail-com/guns-and-knives/dataset/1/)

**Training Achievement:**
*   **Base Model:** YOLOv8s (Small)
*   **Training Set:** 8,000+ Images
*   **Result:** 92.25% mAP50 (Precision: 90%, Recall: 87%)
<img width="664" height="490" alt="image" src="https://github.com/user-attachments/assets/13045801-12a4-46f9-900c-fbb2cec8b626" />
<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/5381f190-8180-4622-ac6a-3d84d5d10465" />
![labels_correlogram](https://github.com/user-attachments/assets/a50ae3be-355b-409f-81e2-06145f2368b4)
![labels](https://github.com/user-attachments/assets/7c9d0c96-15b4-490a-9892-979b105303ef)

---

## 🛠️ How to Run

### 1. Install Dependencies
Ensure you have Python 3.10+ installed.
bash
pip install -r requirements.txt
### 2. Start the AI Agent (The "Eye")
This script connects to the camera (Webcam/RTSP), detects threats, and logs evidence securely.
code
Bash
python guard_agent.py
### 3. Launch the Dashboard (The "Brain")
Open a second terminal to launch the verification interface.
code
Bash
streamlit run dashboard.py
## 🧠 System Architecture (Concept)

1.  **Edge Node:** NVIDIA Jetson / PC runs `guard_agent.py`.
2.  **Inference:** Optimized `.onnx` model scans frames at 30 FPS.
3.  **Trigger:** If Confidence > 50%, the frame is captured.
4.  **Verification:** Image sent to Dashboard.
    *   **CONFIRM:** Alert Police → Image saved to "True Threats" dataset.
    *   **DISMISS:** False Alarm → Image saved to "False Positives" dataset for retraining.
