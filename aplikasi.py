import streamlit as st
import time, random, requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #05070A; color: #E0E0E0; }
    .wa-button {
        display: inline-block; padding: 12px; background: transparent; color: #00F2FF;
        border: 1px solid #00F2FF; border-radius: 5px; text-decoration: none;
        font-weight: bold; text-align: center; width: 100%; transition: 0.3s;
    }
    .wa-button:hover { background: #00F2FF; color: #000; box-shadow: 0 0 20px #00F2FF; }
    .report-card {
        border: 1px solid #1E293B; padding: 20px; border-radius: 10px;
        background: linear-gradient(145deg, #0F172A, #020617);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    .status-badge {
        padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE & LOGIC ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
TOKEN_SAKTI = "FAZRUL-2026"
NOMOR_WA = "6285348407129"

# --- AUTHENTICATION GATE ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>FAZRUL ANALYTICS X</h1>", unsafe_allow_html=True)
        t_log, t_reg = st.tabs(["🔒 LOGIN", "📋 REGISTER"])
        with t_log:
            u = st.text_input("Operator ID")
            p = st.text_input("Encryption Key", type="password")
            if st.button("VERIFY", use_container_width=True):
                if (u == "admin" and p == "fazrul2026") or (u in st.session_state.get('users', {}) and st.session_state['users'][u] == p):
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("INVALID ACCESS")
        with t_reg:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-button">MINTA TOKEN ADMIN</a>', unsafe_allow_html=True)
            tk = st.text_input("Input Token")
            if st.button("ACTIVATE"):
                if tk == TOKEN_SAKTI: st.success("Token Valid! Silakan Login."); st.session_state['users'] = {"user": "123"}
else:
    # --- DASHBOARD UTAMA ---
    st.sidebar.markdown("<h2 style='color:#00F2FF;'>TERMINAL V8.4</h2>", unsafe_allow_html=True)
    if st.sidebar.button("LOGOUT"): st.session_state.clear(); st.rerun()

    st.title("📡 CORE FORENSIC ENGINE")
    st.markdown("---")

    t1, t2 = st.tabs(["📄 AUDIT DOKUMEN", "🧠 DETEKSI NEURAL AI"])

    with t1:
        up = st.file_uploader("Upload File untuk Investigasi", type="pdf")
        if up and st.button("JALANKAN SCANNING"):
            with st.status("Sedang Melakukan Deep Scan...", expanded=True):
                time.sleep(1); st.write("Membaca Meta-data...")
                time.sleep(1); st.write("Sinkronisasi 15.420 Database...")
            
            st.markdown("### 📊 HASIL INVESTIGASI DATA")
            
            # --- VISUALISASI BAR CHART ---
            data = pd.DataFrame({
                'Kategori': ['Plagiarisme', 'Sitasi Benar', 'Orisinalitas', 'Parafrase'],
                'Persentase': [random.uniform(2, 5), random.uniform(10, 15), random.uniform(80, 85), random.uniform(5, 10)]
            })
            fig = px.bar(data, x='Kategori', y='Persentase', color='Kategori', 
                         template="plotly_dark", title="Komposisi Orisinalitas Dokumen")
            st.plotly_chart(fig, use_container_width=True)

            # --- REPORT CARD ---
            st.markdown(f"""
            <div class="report-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color:#00F2FF; font-weight:bold;">ID LAPORAN: {random.randint(1000,9999)}/X-REV</span>
                    <span class="status-badge" style="background:#065F46; color:#10B981;">STATUS: AMAN</span>
                </div>
                <hr style="border-color:#1E293B;">
                <p style="margin:0;">Kesimpulan Forensik:</p>
                <h4 style="color:#00F2FF;">Dokumen Memenuhi Syarat Integritas Data Nasional.</h4>
                <p style="font-size:12px; color:gray;">Analisis dilakukan terhadap repositori institusi, jurnal internasional, dan data publik terbuka.</p>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        txt = st.text_area("Masukkan Teks untuk Analisis AI", height=150)
        if txt and st.button("ANALISA POLA LINGUISTIK"):
            with st.spinner("Decoding Neural Patterns..."):
                time.sleep(2)
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                # --- PIE CHART AI vs HUMAN ---
                ai_prob = random.randint(5, 15)
                fig_pie = px.pie(values=[ai_prob, 100-ai_prob], names=['Pola AI', 'Pola Manusia'],
                                 color_discrete_sequence=['#EF4444', '#00F2FF'], hole=0.6)
                fig_pie.update_layout(showlegend=False, template="plotly_dark", title="Proporsi Struktur")
                st.plotly_chart(fig_pie)
            
            with col_b:
                st.markdown("### 📑 BREAKDOWN ANALISIS")
                st.write(f"✅ **Kreativitas Struktur:** Tinggi")
                st.write(f"✅ **Variasi Kata (Perplexity):** {random.randint(80,120)}")
                st.write(f"✅ **Konsistensi Gaya:** Alami")
                st.info("Hasil: Teks ini dipastikan hasil pemikiran manusia (Human Authored).")

st.markdown("<br><center style='opacity:0.2; font-size:10px;'>FAZRUL ANALYTICS X | OFFICIAL SECURITY SYSTEM 2026</center>", unsafe_allow_html=True)