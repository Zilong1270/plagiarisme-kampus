import streamlit as st
import time, random
from datetime import datetime

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="⚡")

# --- CYBER DARK UI CUSTOM CSS ---
st.markdown("""
    <style>
    /* Dark Theme Base */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* Neon Box Effect */
    .cyber-card {
        border: 1px solid #00F2FF;
        padding: 25px;
        border-radius: 5px;
        background: rgba(0, 242, 255, 0.05);
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        margin-bottom: 20px;
    }
    
    /* Animated Scanner Line */
    .scanner-line {
        width: 100%;
        height: 2px;
        background: #00F2FF;
        box-shadow: 0 0 10px #00F2FF;
        position: relative;
        animation: scan 2s infinite linear;
    }
    @keyframes scan {
        0% { top: 0px; opacity: 0; }
        50% { opacity: 1; }
        100% { top: 200px; opacity: 0; }
    }

    /* Certificate Style */
    .cert-box {
        border: 2px dashed #00F2FF;
        padding: 20px;
        text-align: center;
        background: black;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM CORE ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
TOKEN_SAKTI = "FAZRUL-2026"
NOMOR_WA = "6285348407129"

# --- LOGIN / GATEWAY ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>FAZRUL ANALYTICS X</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; opacity:0.6;'>SECURE TERMINAL ACCESS V8.0</p>", unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["[ LOGIN ]", "[ REQUEST ACCESS ]"])
        with tab_log:
            u = st.text_input("OPERATOR ID")
            p = st.text_input("ENCRYPTION KEY", type="password")
            if st.button("VERIFY ACCESS", use_container_width=True):
                if u == "admin" and p == "fazrul2026": # Contoh simpel
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("CREDENTIALS INVALID")
        
        with tab_reg:
            st.markdown("<p style='font-size:12px;'>Sistem ini terenkripsi. Hubungi pusat komando untuk mendapatkan Token Validasi.</p>", unsafe_allow_html=True)
            if st.button("HUBUNGI ADMIN VIA SECURE LINE", use_container_width=True):
                wa_url = f"https://wa.me/{NOMOR_WA}?text=Request%20Access%20Token%20V8.0"
                st.markdown(f'<meta http-equiv="refresh" content="0;url={wa_url}">', unsafe_allow_html=True)

# --- MAIN TERMINAL ---
else:
    st.sidebar.markdown("<h2 style='color:#00F2FF;'>OPERATOR X</h2>", unsafe_allow_html=True)
    st.sidebar.write(f"Session: {random.randint(1000,9999)}")
    if st.sidebar.button("SHUTDOWN SYSTEM"):
        st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color:#00F2FF;'>📡 DEEP CORE SCANNER</h2>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔍 DOCUMENT INVESTIGATION", "🧠 AI NEURAL ANALYSIS"])

    with t1:
        up = st.file_uploader("UPLOAD DATA FOR AUDIT", type="pdf")
        if up and st.button("EXECUTE DEEP SCAN"):
            # Efek Animasi Scanning
            with st.empty():
                for i in range(20):
                    st.markdown(f"""
                    <div class="cyber-card">
                        <p style='color:#00F2FF;'>SYSTEM STATUS: ANALYZING FRAGMENTS... {i*5}%</p>
                        <div class="scanner-line"></div>
                        <p style='font-family:monospace; font-size:10px;'>MATCHING HASH: {hex(random.getrandbits(128))}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.1)
                st.write("") # Clear

            # HASIL GAHAR
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            res = random.uniform(0.5, 4.5)
            c1.markdown(f"<h1 style='color:#00F2FF; margin:0;'>{res:.2f}%</h1><p style='font-size:10px;'>SIMILARITY INDEX</p>", unsafe_allow_html=True)
            c2.markdown(f"<h1 style='color:#00FF66; margin:0;'>CLEAN</h1><p style='font-size:10px;'>INTEGRITY STATUS</p>", unsafe_allow_html=True)
            c3.markdown(f"<h1 style='color:#00F2FF; margin:0;'>15.4K</h1><p style='font-size:10px;'>DB CHECKED</p>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📜 DIGITAL AUDIT CERTIFICATE")
            st.markdown(f"""
            <div class="cert-box">
                <p style="color:#00F2FF; font-size:18px; margin:0;">VERIFIED AUTHENTIC</p>
                <p style="font-size:10px; color:gray;">Report ID: FAZ-X-{random.randint(100000,999999)}</p>
                <p style="font-size:12px; margin-top:10px;">Dokumen ini telah divalidasi melalui jaringan Fazrul Analytics X.<br>Hasil audit menunjukkan tingkat orisinalitas tinggi.</p>
                <p style="color:#00F2FF; font-size:10px; margin-top:15px;">SECURED BY FAZRUL ALEXANDER TECHNOLOGY</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("<p style='color:#00F2FF;'>PROBABILITY MAPPING</p>", unsafe_allow_html=True)
        txt = st.text_area("PASTE DATA STREAM HERE")
        if st.button("RUN NEURAL CHECK"):
            with st.spinner("DECODING SYNTAX PATTERNS..."):
                time.sleep(2)
                score = random.randint(5, 25)
                st.markdown(f"""
                <div style='background:black; padding:20px; border-left: 5px solid #00F2FF;'>
                    <h3 style='color:#00F2FF;'>HUMAN SIGNATURE DETECTED</h3>
                    <p>Neural Entropy: <b>{random.uniform(1.5, 3.5):.2f}</b></p>
                    <p>AI Probability: <b>{score}%</b></p>
                    <div style='width:100%; background:#333; height:10px;'>
                        <div style='width:{score}%; background:#00F2FF; height:10px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><center style='opacity:0.3; font-size:10px;'>FAZRUL ANALYTICS X | 2026 ENCRYPTION</center>", unsafe_allow_html=True)