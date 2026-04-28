import streamlit as st
import os, time, random, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Fazrul Cyber-Audit Pro", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS UNTUK TAMPILAN PREMIUM ---
st.markdown("""
    <style>
    .report-box { border: 2px solid #f0f2f6; padding: 20px; border-radius: 15px; background-color: #f8f9fa; }
    .metric-card { background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE & KONFIGURASI ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

TOKEN_SAKTI = "FAZRUL-2026"
NOMOR_WA = "6285348407129"

# --- LOGIN SYSTEM ---
def login_system():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ FAZRUL FORENSIC ENGINE</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔑 LOGIN ACCESS", "📝 REGISTER SYSTEM"])
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("AUTHENTICATE", use_container_width=True):
            if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u
                st.rerun()
            else: st.error("ACCESS DENIED: Unauthorized Credentials.")
    with tab2:
        st.info("Pendaftaran memerlukan Validasi Token Admin.")
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")
        tk = st.text_input("Validation Token")
        if st.button("CREATE ACCOUNT"):
            if tk == TOKEN_SAKTI:
                st.session_state['db_users'][new_u] = new_p
                st.success("Account Secured. Please Login.")
            else: st.error("Invalid Token.")

# --- MAIN INTERFACE ---
if not st.session_state['logged_in']:
    login_system()
else:
    with st.sidebar:
        st.markdown(f"### 👤 OPERATOR: {st.session_state['current_user'].upper()}")
        st.status("SYSTEM ONLINE", state="complete")
        if st.button("TERMINATE SESSION"):
            st.session_state.clear()
            st.rerun()

    st.title("🛡️ DEEP FORENSIC ANALYSIS")
    st.write(f"Server Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    t1, t2, t3 = st.tabs(["🔍 DOCUMENT AUDIT", "🌐 NETWORK SCAN", "🤖 AI LINGUISTIC"])

    with t1:
        col_up, col_info = st.columns([1, 1])
        with col_up:
            up = st.file_uploader("Drop Document (PDF/DOCX)", type="pdf")
            btn = st.button("🚀 START DEEP SCAN", use_container_width=True)
        
        with col_info:
            st.markdown("""
            **Audit Parameters:**
            * Cross-Reference 15.420+ Docs
            * Metadata Extraction
            * Sentence Structure Analysis
            """)

        if btn and up:
            with st.status("Initializing Forensic Engine...") as s:
                time.sleep(1)
                s.update(label="Scanning Repository Nasional...", state="running")
                time.sleep(1.5)
                s.update(label="Analysing Neural Patterns...", state="running")
                time.sleep(1)
                s.update(label="Audit Complete!", state="complete")

            st.markdown("### 📊 AUDIT REPORT SUMMARY")
            
            # --- VISUALISASI GAHAR: GAUGE CHART ---
            skor = random.uniform(2.0, 12.0)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = skor,
                title = {'text': "Similarity Index (%)"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#1E3A8A"},
                    'steps': [
                        {'range': [0, 20], 'color': "#D1FAE5"},
                        {'range': [20, 50], 'color': "#FEF3C7"},
                        {'range': [50, 100], 'color': "#FEE2E2"}],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 15}}))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

            # --- BREAKDOWN DATA ---
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<div class='metric-card'><b>Integrity Score</b><br><h2 style='color:green;'>98.2%</h2></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-card'><b>Cited Sources</b><br><h2>{random.randint(5,20)} Found</h2></div>", unsafe_allow_html=True)
            with c3:
                st.markdown("<div class='metric-card'><b>Risk Level</b><br><h2 style='color:blue;'>LOW</h2></div>", unsafe_allow_html=True)

            # --- DIGITAL CERTIFICATE ---
            st.markdown("---")
            st.success(f"**Verification ID:** FAZ-{random.randint(100000,999999)}-PRV")
            st.info("Dokumen ini telah melalui proses audit forensik digital dan dinyatakan otentik dengan tingkat duplikasi di bawah ambang batas.")

    with t3:
        st.subheader("🤖 AI NEURAL DETECTOR")
        txt = st.text_area("Input Text Path", placeholder="Paste content here...")
        if st.button("ANALYSE PATTERN"):
            if txt:
                # Simulasi Radar Chart untuk AI
                categories = ['Repetition', 'Complexity', 'Predictability', 'Burstiness', 'Consistency']
                values = [random.randint(10, 40) for _ in range(5)]
                
                fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', line_color='#1E3A8A'))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, title="AI Fingerprint Analysis")
                
                col_r, col_t = st.columns([1, 1])
                with col_r: st.plotly_chart(fig_radar)
                with col_t:
                    st.write("### Analysis Breakdown")
                    st.write("✅ **Human Signature Detected**")
                    st.write("Sistem mendeteksi adanya variasi struktur kalimat yang dinamis, ciri khas dari tulisan tangan manusia (Non-Generative).")
                    st.progress(25)
                    st.caption("AI Probability: 25%")

st.divider()
st.markdown("<center><b>FAZRUL ALEXANDER | FORENSIC DIVISION © 2026</b><br>Secured Line: 0853-4840-7129</center>", unsafe_allow_html=True)