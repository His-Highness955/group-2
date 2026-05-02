import streamlit as st
import pandas as pd
import numpy as np
import time
import json
import os
import random
import base64
from datetime import datetime
import plotly.graph_objects as go

# --- DATABASE SETUP ---
DB_FILE = "users_db.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_to_db(email, user_data):
    db = load_data()
    db[email] = user_data
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

# ==========================================
# 1. PAGE ARCHITECTURE & STYLING
# ==========================================
st.set_page_config(
    page_title="Group 2 Digital Health Twin App",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Outfit', sans-serif; 
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 15% 50%, #1e1b4b, #0f172a), 
                    linear-gradient(135deg, #0f172a 0%, #172554 100%);
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    .metric-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .auth-card {
        background-color: #172033;
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #2d3748;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    .pulse-container {
        text-align: center;
        padding: 50px;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.5; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.5; }
    }

    .pulse-icon {
        font-size: 80px;
        animation: pulse 2s infinite;
        color: #3b82f6;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .subtext {
        color: #94a3b8;
        font-size: 0.85rem;
    }
    .metric-box {
        background: #1e293b;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #334155;
    }
    .settings-header {
        color: #3b82f6;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }

    h1, h2, h3, p, label { color: #f8fafc !important; }
    .subtext { color: #94a3b8 !important; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if 'user_db' not in st.session_state:
    st.session_state.user_db = {"admin": {"pw": "1234", "name": "Admin User"}}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'page' not in st.session_state:
    st.session_state.page = "Login"
if 'auth_view' not in st.session_state:
    st.session_state.auth_view = 'login'
if 'device_connected' not in st.session_state:
    st.session_state.device_connected = False

# --- AUTHENTICATION UI ---
def login_page():
    user_db = load_data()

    st.markdown("""
    <style>
        .auth-card { 
            background-color: #1e293b; 
            padding: 30px; 
            border-radius: 10px; 
            border: 1px solid #334155; 
            margin-bottom: 20px; 
        }
        .auth-title { 
            text-align: center; 
            font-size: 2rem; 
            font-weight: bold; 
            color: #ffffff; 
            margin-bottom: 5px;
        }
        .auth-subtitle { 
            text-align: center; 
            color: #94a3b8; 
            margin-bottom: 25px; 
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Center the login/registration forms
    _, col, _ = st.columns([1, 1.5, 1])
    
    with col:
        # ==========================================
        # SIGN IN VIEW
        # ==========================================
        if st.session_state.get('auth_view', 'login') == 'login':
            st.markdown("<div style='text-align: center; font-size: 40px; color: #3b82f6;'>💙</div>", unsafe_allow_html=True)
            st.markdown('<div class="auth-title">Welcome Back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Sign in to access your digital twin</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            u = st.text_input("Email Address", placeholder="you@example.com", key="login_email")
            p = st.text_input("Password", placeholder="Enter your password", type="password", key="login_pass")
            
            # Remember me & Forgot password row
            chk_col, link_col = st.columns(2)
            with chk_col:
                st.checkbox("Remember me")
            with link_col:
                st.markdown("<div style='text-align: right; padding-top: 10px;'><a href='#' style='color: #3b82f6; text-decoration: none; font-size: 0.9rem;'>Forgot password?</a></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("➔ Sign In", type="primary", use_container_width=True):
                if u in user_db and user_db[u]['password'] == p:
                    st.session_state.logged_in = True
                    st.session_state.current_user = u
                    st.session_state.user_data = user_db[u] # Load their saved profile info
                    st.session_state.page = "Dashboard"
        
                    st.rerun()
                else:
                    st.error("Account not found or incorrect password.")
            
            st.markdown("""
                <div style='text-align: center; margin: 20px 0;'>
                    <span style='color: #64748b; font-size: 0.9rem;'>New to Health Twin?</span>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Create Account", use_container_width=True):
                st.session_state.auth_view = 'register'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ==========================================
        # CREATE ACCOUNT VIEW
        # ==========================================
        else:
            st.markdown('<div class="auth-title">Create Account</div><br>', unsafe_allow_html=True)
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Full Name", placeholder="John Doe")
            with c2:
                new_dob = st.date_input("Date of Birth", value=datetime.date(2000, 1, 1))

            new_email = st.text_input("Email Address", placeholder="you@example.com", key="reg_email")
    
            c3, c4 = st.columns(2)
            with c3:
                new_pw = st.text_input("Password", type="password", key="reg_pass", placeholder="Enter your password")
            with c4:
                confirm_pw = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            st.markdown("<div style='color: #64748b; font-size: 0.75rem; margin-top: -10px; margin-bottom: 15px;'>Password must contain: At least 6 characters, 1 capital letter, and 1 special character.</div>", unsafe_allow_html=True)
            
            # Row 4: Medical History
            medical_history = st.text_area("Medical History (Optional)", placeholder="Allergies, past conditions...", height=100)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Row 5: Action Buttons
            b1, b2 = st.columns(2)
            with b1:
                if st.button("← Back to Login", use_container_width=True):
                    st.session_state.auth_view = 'login'
                    st.rerun()
            with b2:
                if st.button("✔ Create Account", type="primary", use_container_width=True):
                    if new_email and new_pw:
                        if new_pw == confirm_pw:
                            # Package the user data and save to JSON

                            user_data = {
                                "name": new_name,
                                "dob": str(new_dob),
                                "password": new_pw,
                                "medical_history": medical_history,
                                "height": 0,
                                "weight": 0
                            }
                            save_user_to_db(new_email, user_data)
                            
                            st.success("Account created successfully! You can now log in.")
                            st.session_state.auth_view = 'login'
                        else:
                            st.error("Passwords do not match!")
                    else:
                        st.warning("Please fill in the required email and password fields.")
            st.markdown('</div>', unsafe_allow_html=True)

def sidebar_nav():
    with st.sidebar:
        st.markdown("💙 Digital Health Twin")
        st.markdown("---")
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.page = "Dashboard"
        if st.button("➕ Add Data", use_container_width=True): st.session_state.page = "Add Data"
        if st.button("🔬 Analysis", use_container_width=True): st.session_state.page = "Analysis"
        if st.button("📁 Upload", use_container_width=True): st.session_state.page = "Upload"
        if st.button("⌚ Devices", use_container_width=True): st.session_state.page = "Devices" # NEW
        if st.button("⚙️ Settings", use_container_width=True): st.session_state.page = "Settings"
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "Login"
            st.rerun()

def dashboard_view():
    st.title("Dashboard")
    col_left, col_right = st.columns([1, 2.5])
    
    user = st.session_state.user_data

    with col_left:
        # Profile Card
        st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:50px; background:#3b82f630; width:80px; height:80px; line-height:80px; border-radius:50%; margin:0 auto 10px;">👤</div>
                <h3>{user['name']}</h3>
                <p class="subtext">Active Session: Verified</p>
            </div>
        """, unsafe_allow_html=True)
        
        # FUNCTIONAL EDIT BUTTON
        if st.button("Edit Profile", use_container_width=True):
            st.session_state.page = "Settings"
            st.rerun()

        # Health Score Card
        st.markdown(f"""
            <div class="glass-card">
                <p style="font-weight:600;">Health Score <span style="float:right;">🤍</span></p>
                <h1 style="margin:0;">100 <span style="font-size:1rem; color:#94a3b8;">/ 100</span></h1>
                <div style="width:100%; height:8px; background:#334155; border-radius:10px; margin:15px 0;">
                    <div style="width:100%; height:100%; background:#3b82f6; border-radius:10px;"></div>
                </div>
                <p class="subtext">Your digital twin indicates optimal health.</p>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Action Buttons
        t1, t2, t3, t4 = st.columns(4)
        if t1.button("➕\n\nAdd Vitals", use_container_width=True): st.session_state.page = "Add Data"; st.rerun()
        if t2.button("📁\n\nUpload Doc", use_container_width=True): st.session_state.page = "Upload"; st.rerun()
        if t3.button("🔬\n\nAnalysis", use_container_width=True): st.session_state.page = "Analysis"; st.rerun()
        if t4.button("⌚\n\nDevices", use_container_width=True): st.session_state.page = "Devices"; st.rerun()
            
        st.markdown("📑 Key Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown('<div class="metric-box"><p class="subtext">BP</p><h4>120/80</h4></div>', unsafe_allow_html=True)
        m2.markdown('<div class="metric-box"><p class="subtext">Heart Rate</p><h4>72 bpm</h4></div>', unsafe_allow_html=True)
        m3.markdown('<div class="metric-box"><p class="subtext">Sleep</p><h4>7.5 hrs</h4></div>', unsafe_allow_html=True)
        weight_display = st.user.get("weight", "0") 
        m4.markdown(f'<div class="metric-box"><p class="subtext">Weight</p><h4>{weight_display} kg</h4></div>', unsafe_allow_html=True)
        
        st.markdown("<br> 💡 Recent Insights", unsafe_allow_html=True)
        st.markdown('<div class="glass-card" style="text-align:center; opacity:0.6;">'
                    '<div>🗄️</div><p class="subtext">No insights generated yet. Add health data to start.</p></div>', unsafe_allow_html=True)

def device_connection_page():
    st.title("Device Sync & Telemetry")
    
    # Initialize connection state if it doesn't exist
    if 'device_connected' not in st.session_state:
        st.session_state.device_connected = False

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📡 Connect Wearable")
        st.markdown("<p class='subtext'>Initialize to sync live biological telemetry to your digital twin.</p>", unsafe_allow_html=True)
        
        device_choice = st.selectbox("Select Device", ["if connected to a smart watch","Apple Watch Ultra", "Garmin Fenix 7", "Oura Ring Gen 3", "Samsung Galaxy Watch 6"])
        
        if not st.session_state.device_connected:
            if st.button("🔄 Initiate BLE Sync", type="primary", use_container_width=True):
                with st.spinner(f"Establishing secure connection with {device_choice}..."):
                    time.sleep(2) # Simulate connection delay
                st.session_state.device_connected = True
                st.rerun()
        else:
            st.success(f"Connected to {device_choice}")
            if st.button("Disconnect", use_container_width=True):
                st.session_state.device_connected = False
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if st.session_state.device_connected:
            st.markdown("❤️ Live Vitals")
            v1, v2, v3 = st.columns(3)
            with v1:
                st.markdown('<div class="glass-card" style="text-align:center; padding:15px;"><p class="subtext" style="margin:0;">Heart Rate</p><h2 style="margin:0; color:#ef4444;">74 <span style="font-size:1rem;">bpm</span></h2></div>', unsafe_allow_html=True)
            with v2:
                st.markdown('<div class="glass-card" style="text-align:center; padding:15px;"><p class="subtext" style="margin:0;">Blood Pressure</p><h2 style="margin:0; color:#3b82f6;">118/76</h2></div>', unsafe_allow_html=True)
            with v3:
                st.markdown('<div class="glass-card" style="text-align:center; padding:15px;"><p class="subtext" style="margin:0;">Last Sleep</p><h2 style="margin:0; color:#a855f7;">7h 12m</h2></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Exercise Activity Section
            st.markdown(" 🏃‍♂️ Recent Activities")
            
            # Tab layout for different exercises
            tab1, tab2, tab3 = st.tabs(["Jogging", "Cycling", "Swimming"])
            
            with tab1:
                st.markdown("""
                <div class="glass-card" style="margin-top:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div><h4 style="margin:0;">Morning Run</h4><p class="subtext" style="margin:0;">Today, 6:30 AM</p></div>
                        <h3 style="margin:0; color:#10b981;">5.2 km</h3>
                    </div>
                    <hr style="border-color:#334155; margin:10px 0;">
                    <div style="display:flex; justify-content:space-between;">
                        <span>⏱️ Duration: 28:45</span>
                        <span>🔥 Burned: 320 kcal</span>
                        <span>👟 Pace: 5'31"/km</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with tab2:
                st.markdown("""
                <div class="glass-card" style="margin-top:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div><h4 style="margin:0;">Evening Ride</h4><p class="subtext" style="margin:0;">Yesterday, 5:15 PM</p></div>
                        <h3 style="margin:0; color:#f59e0b;">15.4 km</h3>
                    </div>
                    <hr style="border-color:#334155; margin:10px 0;">
                    <div style="display:flex; justify-content:space-between;">
                        <span>⏱️ Duration: 45:10</span>
                        <span>🔥 Burned: 410 kcal</span>
                        <span>🚴 Avg Speed: 20.5 km/h</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with tab3:
                st.markdown("""
                <div class="glass-card" style="margin-top:10px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div><h4 style="margin:0;">Pool Session</h4><p class="subtext" style="margin:0;">Tuesday, 7:00 AM</p></div>
                        <h3 style="margin:0; color:#0ea5e9;">1,200 m</h3>
                    </div>
                    <hr style="border-color:#334155; margin:10px 0;">
                    <div style="display:flex; justify-content:space-between;">
                        <span>⏱️ Duration: 35:00</span>
                        <span>🏊 Laps: 48</span>
                        <span>💧 SWOLF: 34</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="glass-card" style="text-align:center; padding:100px; opacity:0.5;">
                    <div style="font-size:50px; margin-bottom:15px;">🔗</div>
                    <h4>No Device Connected</h4>
                    <p class="subtext">Initiate a sync on the left to view live telemetry.</p>
                </div>
            """, unsafe_allow_html=True)

def add_data_page():
    st.title("Add Health Data")
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.text_input("Blood Pressure (mmHg)", placeholder="e.g. 120/80")
        c1.number_input("Weight (kg)", value=70.0)
        c2.number_input("Heart Rate (bpm)", value=72)
        c2.number_input("Sleep (hrs)", value=8.0)
        st.text_area("Symptoms / Notes", placeholder="How are you feeling today?")
        if st.button("✔ Submit & Analyze", type="primary"): 
            st.success("Data Synthesized to Twin!")
            time.sleep(1)
            st.session_state.page = "Dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def upload_page():
    st.title("Upload Documents")
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.selectbox("Document Type", ["Lab Report", "Prescription", "Radiology", "Other"])
        st.file_uploader("Upload medical document or take a photo")
        st.button("Extract Data", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card" style="height: 300px; display: flex; flex-direction: column; justify-content: center; align-items: center; opacity: 0.5;">'
                    '<h4>Extracted Information</h4><p class="subtext">Upload a document to see results</p></div>', unsafe_allow_html=True)

def analysis_page():
    st.title("Detailed Analysis")
    st.markdown("""
        <div class="glass-card" style="text-align:center; padding:100px;">
            <div style="font-size:60px;">🔬</div>
            <h3>No Analysis Available</h3>
            <p class="subtext">Add health data or link a device to generate your digital twin analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Add Health Data"):
        st.session_state.page = "Add Data"
        st.rerun()

def settings_page():
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

    st.markdown("<h1 style='color: white;'>Account Settings</h1>", unsafe_allow_html=True)

    # --- 2. STYLING (Internal CSS) ---
    st.markdown("""
    <style>
        .settings-header {
            color: #3b82f6;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 20px 0 10px 5px;
        }
        .info-box {
            background: rgba(168, 85, 247, 0.1);
            border: 1px solid #a855f7;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user_data", {})

    # --- 3. ACCOUNT SECTION ---
    st.markdown("<div class='settings-header'>👤 Account Information</div>", unsafe_allow_html=True)
    with st.container(border=True):
        new_name = st.text_input("Full Name", value=user.get("name", ""))
        # Use .get() for email in case it's missing from the JSON
        new_email = st.text_input("Email Address", value=user.get("email", st.session_state.get("current_user", "")))
        new_pass = st.text_input("Change Password", value=user.get("password", ""), type="password")

    # --- 4. HEALTH SECTION ---
    st.markdown("<div class='settings-header'>⚖️ Health Metrics</div>", unsafe_allow_html=True)
    with st.container(border=True):
    try:
        dob_str = user.get("dob", "2000-01-01")
        if isinstance(dob_str, str):
            dob_val = datetime.datetime.strptime(dob_str, '%Y-%m-%d')
        else:
            dob_val = dob_str # It's already a date object
    except Exception:
        dob_val = datetime.date(2000, 1, 1)  
            
        new_dob = st.date_input("Date of Birth", value=dob_val)
        
        c1, c2 = st.columns(2)
        with c1:
            new_height = st.number_input("Height (cm)", value=float(user.get("height", 0)))
        with c2:
            new_weight = st.number_input("Weight (kg)", value=float(user.get("weight", 0)))

    # --- 5. SAVE CHANGES ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Save All Changes", type="primary", use_container_width=True):
        # Update session state
        st.session_state.user_data.update({
            "name": new_name,
            "email": new_email,
            "password": new_pass,
            "dob": str(new_dob),
            "height": new_height,
            "weight": new_weight
        })
        # Save to permanent JSON database
        save_user_to_db(st.session_state.current_user, st.session_state.user_data)
        st.success("Profile updated successfully!")
        time.sleep(1)
        st.rerun()

    # --- 6. ABOUT SECTION (Expander) ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("ℹ️ About App"):
        st.markdown(f"""
            <div class="info-box">
                <h3 style="color:#a855f7; margin-bottom: 5px;">Group 2: Digital Health Twin</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Research Project - CSC 309</p>
                <hr style="border-color: rgba(168,85,247,0.3); margin: 15px 0;">
                <b style="color: white;">Objective:</b> 
                <span style="color: #cbd5e1;">Real-time biological telemetry synthesis. <br> That shows real time health insights.</span>
                <p style="color: #64748b; font-size: 0.8rem; margin-top: 15px; font-style: italic;">
                    Instructor: Mrs. T.O. Adefehinti
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- 7. LOGOUT ---
    if st.button("↪ Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.rerun()

# ==========================================
# 4. ROUTING LOGIC
# ==========================================
if not st.session_state.logged_in:
    login_page()
else:
    sidebar_nav()
    current_page = st.session_state.get('page', 'Dashboard')

    if current_page == "Dashboard":
        dashboard_view()
    elif current_page == "Add Data":
        add_data_page()
    elif current_page == "Upload":
        upload_page()
    elif current_page == "Analysis":
        analysis_page()
    elif current_page == "Devices":
        device_connection_page()
    elif current_page == "Settings":
        settings_page() 
    elif current_page.lower() == "login":
        st.session_state.logged_in = False
        st.rerun()
    else:
        st.session_state.page = "Dashboard"
        st.rerun()
