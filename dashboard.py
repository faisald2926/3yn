import streamlit as st
import os
import time
import shutil
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="3yn Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONSTANTS & SETUP ---
BASE_DIR = os.getcwd()
ALERT_FOLDER = os.path.join(BASE_DIR, "alerts")

# 1. Confirmed Threats Paths
TRAIN_TRUE_ROOT = os.path.join(BASE_DIR, "training_data", "true_alarms")
TRAIN_TRUE_IMAGES = os.path.join(TRAIN_TRUE_ROOT, "images")
TRAIN_TRUE_LABELS = os.path.join(TRAIN_TRUE_ROOT, "labels")

# 2. False Alarms Paths
TRAIN_FALSE_ROOT = os.path.join(BASE_DIR, "training_data", "false_alarms")
TRAIN_FALSE_IMAGES = os.path.join(TRAIN_FALSE_ROOT, "images")
TRAIN_FALSE_LABELS = os.path.join(TRAIN_FALSE_ROOT, "mistake_label")

# Ensure ALL directories exist
for f in [ALERT_FOLDER, TRAIN_TRUE_IMAGES, TRAIN_TRUE_LABELS, TRAIN_FALSE_IMAGES, TRAIN_FALSE_LABELS]:
    os.makedirs(f, exist_ok=True)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    header[data-testid="stHeader"] { background-color: transparent; }
    
    /* Processed Card Effect */
    .processed-card { opacity: 0.6; filter: grayscale(100%); }
    
    /* Status Badge Styling - Matches Button Height */
    .status-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 45px; /* Exact height of Streamlit buttons */
        border-radius: 8px;
        font-weight: 700;
        font-family: sans-serif;
        margin-top: 0px; 
        width: 100%;
    }
    
    .status-confirmed {
        background-color: #b91c1c; /* RED-700 */
        color: white; 
        border: 1px solid #7f1d1d;
    }
    
    .status-dismissed {
        background-color: #334155; /* SLATE-700 */
        color: #94a3b8; 
        border: 1px solid #475569;
    }

    /* Button Overrides */
    div.stButton > button { 
        height: 45px; 
        width: 100%; 
        border-radius: 8px; 
        border: none; 
        font-weight: 600; 
    }
    button[kind="primary"] { background-color: #dc2626 !important; color: white !important; }
    button[kind="secondary"] { background-color: #1e293b !important; border: 1px solid #334155 !important; color: #e2e8f0 !important;}
    
    .overlay-tag { background-color: rgba(0,0,0,0.6); color: white; padding: 2px 8px; border-radius: 4px; font-family: monospace; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def handle_action(alert_id, is_valid, file_path):
    """Moves training files but KEEPS display file."""
    
    base_filename = os.path.basename(file_path) # alert_123_display.jpg
    dir_name = os.path.dirname(file_path)       # .../alerts/

    # Construct names
    clean_base = base_filename.replace("_display", "") 
    clean_img_name = clean_base
    label_name = clean_base.replace(".jpg", ".txt").replace(".png", ".txt")

    # Source Paths
    src_clean = os.path.join(dir_name, clean_img_name)
    src_label = os.path.join(dir_name, label_name)

    # Destination Paths Logic
    if is_valid:
        # TRUE -> true_alarms/images AND true_alarms/labels
        dst_clean = os.path.join(TRAIN_TRUE_IMAGES, clean_img_name)
        dst_label = os.path.join(TRAIN_TRUE_LABELS, label_name)
        
        st.session_state.stats['true'] += 1
        st.toast("Confirmed: Threat Logged", icon="🚨")
    else:
        # FALSE -> false_alarms/images AND false_alarms/mistake_label
        dst_clean = os.path.join(TRAIN_FALSE_IMAGES, clean_img_name)
        dst_label = os.path.join(TRAIN_FALSE_LABELS, label_name)
        
        st.session_state.stats['false'] += 1
        st.toast("Dismissed: Model Updated", icon="🛡️")

    # MOVE FILES (Only Clean & Label, Display stays!)
    try:
        if os.path.exists(src_clean): shutil.move(src_clean, dst_clean)
        if os.path.exists(src_label): shutil.move(src_label, dst_label)
        
        # Mark as processed in session state so UI updates instantly
        st.session_state.processed_status[alert_id] = "CONFIRMED" if is_valid else "DISMISSED"
        
    except Exception as e:
        st.error(f"Error moving files: {e}")

def load_data():
    """
    Loads files. 
    Logic: If 'clean' image exists -> PENDING. 
    If 'clean' image missing but 'display' exists -> PROCESSED.
    """
    DISPLAY_SUFFIX = "_display"
    IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg')
    
    all_files = os.listdir(ALERT_FOLDER)
    alerts = []
    
    # Filter for display images
    display_files = [f for f in all_files if f.endswith(IMAGE_EXTENSIONS) and DISPLAY_SUFFIX in f]
    
    # Sort newest first
    display_files.sort(key=lambda f: os.path.getmtime(os.path.join(ALERT_FOLDER, f)), reverse=True)

    for f in display_files:
        alert_id = f.split('.')[0] # alert_timestamp_display
        full_path = os.path.join(ALERT_FOLDER, f)
        
        # Check if Clean Image exists
        clean_name = f.replace(DISPLAY_SUFFIX, "")
        clean_path = os.path.join(ALERT_FOLDER, clean_name)
        
        # Determine Status
        status = "PENDING"
        if not os.path.exists(clean_path):
            # If clean file is gone, check our session history
            status = st.session_state.processed_status.get(alert_id, "ARCHIVED")

        alerts.append({
            "id": alert_id,
            "timestamp": time.ctime(os.path.getmtime(full_path)),
            "camera": "LIVE-FEED",
            "path": full_path,
            "status": status
        })
    
    return alerts

# --- INITIALIZATION ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'true': 0, 'false': 0}
if 'processed_status' not in st.session_state:
    st.session_state.processed_status = {}
if 'last_file_count' not in st.session_state:
    st.session_state.last_file_count = 0

# --- SIDEBAR UI ---
def sidebar_ui(alerts):
    with st.sidebar:
        st.markdown("### 🛡️ 3yn Command")
        
        pending_count = sum(1 for a in alerts if a['status'] == "PENDING")
        
        c1, c2 = st.columns(2)
        c1.metric("Active", pending_count)
        c2.metric("Dataset", st.session_state.stats['true'] + st.session_state.stats['false'])
        
        st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)
        st.markdown("---")
        
        st.caption("🔴 SYSTEM ACTIVE (Monitoring)")
        
        if st.button("Reset / Logout", type="secondary", use_container_width=True):
            st.session_state.clear()
            st.rerun()

# --- MAIN APP ---
def main():
    # Load Data
    alerts = load_data()
    sidebar_ui(alerts)

    # UI HEADER
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <div class='custom-header'>Sector 7 Monitoring</div>
            <div class='custom-subhead'>{'Threats Detected' if any(a['status'] == 'PENDING' for a in alerts) else 'All Clear'}</div>
        </div>
        <div style='text-align: right; font-family: monospace; color: #cbd5e1; font-size: 12px;'>
            SYSTEM_ID: 3YN-CMD-01
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not alerts:
        st.markdown("<div style='text-align:center; padding: 50px; color: #475569;'><h2>✅ No Activity</h2></div>", unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, alert in enumerate(alerts):
            col = cols[i % 3]
            with col:
                is_processed = alert['status'] != "PENDING"
                
                # Apply visual dimming if processed
                container_style = "opacity: 0.5;" if is_processed else ""
                
                with st.container(border=True):
                    # Header
                    st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; font-size: 12px; color: #60a5fa; {container_style}'>
                        <span>{alert['id'][-6:]}</span>
                        <span style='color: #cbd5e1'>{alert['timestamp'].split()[3]}</span> 
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Image
                    st.image(alert['path'], use_container_width=True)
                    
                    # OVERLAY & CONTROLS
                    if is_processed:
                        # Show Colored Badge (Height matched to buttons)
                        class_name = "status-confirmed" if "CONFIRM" in alert['status'] else "status-dismissed"
                        text = "THREAT CONFIRMED" if "CONFIRM" in alert['status'] else "FALSE ALARM"
                        st.markdown(f"""
                        <div class='status-badge {class_name}'>
                            {text}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Show Buttons
                        st.markdown(f"<div class='overlay-tag' style='margin-top: -30px; position: relative;'>{alert['camera']}</div>", unsafe_allow_html=True)
                        st.write("") # Spacer
                        
                        # Use gap="small" to tighten the space between buttons
                        b1, b2 = st.columns(2, gap="small")
                        with b1:
                            # use_container_width=True forces button to fill the column
                            if st.button("CONFIRM", key=f"c_{alert['id']}", type="primary", use_container_width=True):
                                handle_action(alert['id'], True, alert['path'])
                                st.rerun()
                        with b2:
                            if st.button("DISMISS", key=f"d_{alert['id']}", type="secondary", use_container_width=True):
                                handle_action(alert['id'], False, alert['path'])
                                st.rerun()

    # --- WATCHDOG LOOP (Silent Refresh) ---
    current_count = len(os.listdir(ALERT_FOLDER))
    if current_count != st.session_state.last_file_count:
        st.session_state.last_file_count = current_count
    
    while True:
        time.sleep(1) # Check every 1 second
        new_count = len(os.listdir(ALERT_FOLDER))
        if new_count != st.session_state.last_file_count:
            st.rerun()

if __name__ == "__main__":
    main()
