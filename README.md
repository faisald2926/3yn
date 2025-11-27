# 👁️ 3yn (Ein): Autonomous Weapon Detection & Response System

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
*   **Training Set:** 4,000+ Images
*   **Result:** 92.25% mAP50 (Precision: 90%, Recall: 87%)

---

## 🛠️ How to Run

### 1. Install Dependencies
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
