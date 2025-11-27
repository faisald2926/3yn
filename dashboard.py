import streamlit as st
import os
import time
import shutil

st.set_page_config(page_title="3yn Command", page_icon="🛡️", layout="wide")

# --- FOLDERS ---
ALERT_FOLDER = "alerts"
# We separate images and labels for standard YOLO training structure
TRAIN_TRUE_IMG = "training_data/true_alarms/images"
TRAIN_TRUE_LBL = "training_data/true_alarms/labels"
TRAIN_FALSE = "training_data/false_alarms"

for f in [ALERT_FOLDER, TRAIN_TRUE_IMG, TRAIN_TRUE_LBL, TRAIN_FALSE]:
    if not os.path.exists(f): os.makedirs(f)

# --- STYLE ---
st.markdown("""
<style>
    div[data-testid="stImage"] img { height: 220px; object-fit: cover; border-radius: 8px; }
    div[data-testid="stVerticalBlock"] > div { background-color: #1E1E1E; border: 1px solid #333; border-radius: 12px; padding: 15px; }
    button:first-child { background-color: #FF4B4B; color: white; font-weight: bold; border: none; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC: HANDLE DATA ---
def process_alert(base_name, is_valid):
    # File paths
    display_img = os.path.join(ALERT_FOLDER, f"{base_name}_display.jpg")
    clean_img   = os.path.join(ALERT_FOLDER, f"{base_name}.jpg")
    label_txt   = os.path.join(ALERT_FOLDER, f"{base_name}.txt")
    
    if is_valid:
        # 1. Move CLEAN image to training images
        if os.path.exists(clean_img):
            shutil.move(clean_img, os.path.join(TRAIN_TRUE_IMG, f"{base_name}.jpg"))
            
        # 2. Move TEXT label to training labels
        if os.path.exists(label_txt):
            shutil.move(label_txt, os.path.join(TRAIN_TRUE_LBL, f"{base_name}.txt"))
            
    else:
        # False Alarm: Move CLEAN image to negative samples
        if os.path.exists(clean_img):
            shutil.move(clean_img, os.path.join(TRAIN_FALSE, f"{base_name}.jpg"))
        # Delete the incorrect label text
        if os.path.exists(label_txt): os.remove(label_txt)

    # 3. Always delete the "Display" image (it was just for the human)
    if os.path.exists(display_img): os.remove(display_img)

# --- UI ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'

if st.session_state.page == 'welcome':
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.title("👁️ 3yn Intelligence")
        st.caption("Autonomous Threat Detection & Active Learning")
        if st.button("Initialize Agent", type="primary", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
else:
    with st.sidebar:
        st.header("3yn HQ")
        # Filter to show only display images
        display_files = [f for f in os.listdir(ALERT_FOLDER) if "_display.jpg" in f]
        display_files.sort(reverse=True)
        
        col1, col2 = st.columns(2)
        col1.metric("Active", len(display_files))
        col2.metric("Learned", len(os.listdir(TRAIN_TRUE_IMG)))
        
        if st.button("Clear All", use_container_width=True):
            # Nuke everything in alerts folder
            for f in os.listdir(ALERT_FOLDER):
                try: os.remove(os.path.join(ALERT_FOLDER, f))
                except: pass
            st.rerun()
            
        if st.button("Logout"): st.session_state.page = 'welcome'; st.rerun()

    st.subheader("Live Threat Stream")

    if not display_files:
        st.success("Sector Secure.")
    else:
        cols = st.columns(3)
        for idx, file_name in enumerate(display_files):
            # Extract base ID (e.g. "alert_2023..." from "alert_2023..._display.jpg")
            base_id = file_name.replace("_display.jpg", "")
            file_path = os.path.join(ALERT_FOLDER, file_name)
            
            with cols[idx % 3]:
                with st.container():
                    try:
                        st.image(file_path, use_container_width=True)
                    except: continue
                    
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("CONFIRM", key=f"c_{idx}", use_container_width=True):
                            process_alert(base_id, True)
                            st.toast("Threat Confirmed. Data moved to training.", icon="🚨")
                            time.sleep(0.2)
                            st.rerun()
                    with b2:
                        if st.button("Dismiss", key=f"d_{idx}", use_container_width=True):
                            process_alert(base_id, False)
                            st.toast("False Alarm. AI updated.", icon="✅")
                            time.sleep(0.2)
                            st.rerun()
    
    time.sleep(1)
    st.rerun()