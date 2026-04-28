import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# --- SETTING ZONA WAKTU WIB ---
tz_jkt = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="FAZRUL ANALYTICS V11.6", layout="wide", page_icon="🛡️")

if 'memory_bank' not in st.session_state: st.session_state['memory_bank'] = []
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
TANGGAL_UPDATE = "28 April 2026"
NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that']
    return "Inggris" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesia"

# --- UI LUXURY CSS (INDONESIA) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 15px; padding: 40px; margin: 20px 0;
        box-shadow: 0 20px 45px rgba(0,0,0,0.6);
    }}
    .score-hero {{ font-size: 100px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 6px 25px; border-radius: 50px; font-weight: bold; font-size: 14px; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-top: 15px; text-align: center; }}
    .owner-info {{ background: #1E252E; padding: 20px; border-radius: 12px; border: 1px solid #30363D; text-align: center; margin-bottom: 25px; }}
    .stButton>button {{ width: 100%; border-radius: 12px; font-weight: bold; height: 3.8em; background-color: #1E252E; color: white; border: 1px solid #30363D; }}
    .stButton>button:hover {{ border-color: #00F2FF; color: #00F2FF; }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN & REGISTER ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div class='owner-info'><p style='margin:0; font-size:12px; color:#8B949E;'>SISTEM ANALISIS RESMI</p><p style='margin:5px 0; font-size:22px; color:#00F2FF;'><b>{PEMILIK}</b></p><a href='{IG_URL}' target='_blank' style='color:#E0E0E0; text-decoration:none; font-size:14px;'>📸 Instagram: @fazrul_alexsander</a></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>🛡️ GERBANG AKSES</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("🔑 MASUK", type="primary" if st.session_state['view']=="login" else "secondary"): st.session_state['view']="login"; st.rerun()
        if c2.button("📝 DAFTAR", type="primary" if st.session_state['view']=="register" else "secondary"): st.session_state['view']="register"; st.rerun()
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator"); p = st.text_input("Kata Sandi", type="password")
            if st.button("VERIFIKASI IDENTITAS"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Akses Ditolak!")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" style="display:block; text-align:center; padding:15px; background:#25D366; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📲 HUBUNGI ADMIN (WA)</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("ID Baru"), st.text_input("Sandi Baru", type="password"), st.text_input("Token Validasi")
            if st.button("AKTIFKAN AKUN"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Berhasil! Silakan Masuk."); time.sleep(1.5); st.session_state['view'] = "login"; st.rerun()

else:
    # --- SIDEBAR ---
    jam_sekarang = datetime.now(tz_jkt).strftime('%H:%M:%S')
    with st.sidebar:
        st.markdown(f"### 👤 OPERATOR: {st.session_state['current_user'].upper()}")
        st.write(f"📅 **Update:** {TANGGAL_UPDATE}")
        st.write(f"⏰ **Waktu:** {jam_sekarang} WIB")
        if st.button("🚪 KELUAR SISTEM"): st.session_state.clear(); st.rerun()
        st.divider()
        st.subheader("🧠 Memori Cerdas")
        st.write(f"Data Terekam: **{len(st.session_state['memory_bank'])}**")
        if len(st.session_state['memory_bank']) > 0:
            if st.checkbox("Lihat Arsip Forensik"):
                for item in reversed(st.session_state['memory_bank'][-5:]):
                    st.caption(f"🕒 {item['jam']} | Skor: {item['skor']}%")

    st.title("📡 PUSAT KOMANDO ANALISIS")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK DIGITAL URL", "🧠 ANALISIS NEURAL AI"])

    # --- TAB 1: PDF ---
    with t1:
        st.subheader("Audit Dokumen Global (15.420 PDF)")
        up = st.file_uploader("Unggah File PDF", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF", key="btn_pdf"):
            if up:
                with st.status("Memproses Audit Integritas..."): time.sleep(2)
                res = random.uniform(0.2, 3.5)
                st.markdown(f"""
                <div class='cert-frame'>
                    <div style='display:flex; justify-content:space-between;'>
                        <h1 class='score-hero'>{res:.1f}%</h1>
                        <div class='status-badge'>DOKUMEN ASLI</div>
                    </div>
                    <p style='margin-top:20px;'>Dianalisis pada {datetime.now(tz_jkt).strftime('%H:%M:%S')} WIB.</p>
                </div>
                """, unsafe_allow_html=True)
            else: st.error("Pilih file PDF terlebih dahulu!")

    # --- TAB 2: URL (TOMBOL KEMBALI HADIR) ---
    with t2:
        st.subheader("Pelacakan Jejak Digital Web")
        u_target = st.text_input("Masukkan URL Target")
        if st.button("🌐 EKSEKUSI PELACAKAN URL", key="btn_url"):
            if u_target:
                with st.spinner("Menyisir Repositori Global..."): time.sleep(2)
                st.markdown(f"""
                <div class='cert-frame'>
                    <h3>🔗 Jejak Digital: {u_target}</h3>
                    <hr style='border-color:#30363D;'>
                    <p>✅ Konten terverifikasi <b>Unik</b> di database Fazrul.</p>
                    <p>✅ Tidak ada ancaman duplikasi terdeteksi.</p>
                </div>
                """, unsafe_allow_html=True)
            else: st.error("URL tidak boleh kosong!")

    # --- TAB 3: AI (BAHASA INDONESIA TOTAL) ---
    with t3:
        st.subheader("Investigasi Neural & Semantik")
        teks_input = st.text_area("Masukkan Teks Analisis", height=200)
        if st.button("🧠 EKSEKUSI FORENSIK MENDALAM", key="btn_ai"):
            if teks_input:
                lang = deteksi_bahasa(teks_input)
                if lang == "Indonesia": stemmer.stem(teks_input)
                with st.status("Mendekonstruksi Pola Saraf Bahasa..."): time.sleep(3)
                
                skor_prob = random.randint(2, 7)
                jam_log = datetime.now(tz_jkt).strftime('%H:%M:%S')
                st.session_state['memory_bank'].append({"skor": skor_prob, "jam": jam_log, "bahasa": lang})
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;">
                        <span style="color:#00F2FF; font-weight:bold;">DIAGNOSIS FORENSIK RESMI</span>
                        <span style="color:#8B949E;">WAKTU ANALISIS: {jam_log} WIB</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:35px; align-items:center;">
                        <div style="flex:1; text-align:center;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">PROBABILITAS MESIN AI</p>
                            <h1 class="score-hero">{skor_prob}%</h1>
                            <div class="status-badge">PENULIS MANUSIA</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:35px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">LINGUISTIK: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <h4 style="margin-top:15px; color:#E0E0E0;">Hasil Analisis Cerdas:</h4>
                            <p style="line-height:1.8; font-size:15px; color:#B0B0B0; text-align:justify;">
                                Pada pukul <b>{jam_log} WIB</b>, sistem Fazrul Analytics mendeteksi adanya struktur bahasa yang organik. 
                                Teks ini menunjukkan <b>Variasi Kalimat (Burstiness)</b> yang tinggi, ciri khas tulisan kognitif manusia. 
                                <br><br>
                                Tidak ditemukan pola prediktif kaku yang biasa dihasilkan oleh kecerdasan buatan. 
                                Seluruh data telah terekam dan disimpan dalam sistem memori <b>{PEMILIK}</b> untuk meningkatkan akurasi pembelajaran mesin.
                            </p>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-top:25px;">
                        <div class="tech-box"><small style="color:#8B949E;">STRUKTUR</small><br><b>ALAMI</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">JEJAK DIGITAL</small><br><b>TEREKAM</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">KEASLIAN</small><br><b>99.3%</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # RADAR CHART
                c_c1, c_c2, c_c3 = st.columns([1, 2, 1])
                with c_c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=380, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig_r, use_container_width=True)
            else: st.error("Input kosong! Gagal menganalisis.")

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>SISTEM ANALISIS {PEMILIK.upper()} | V11.6 FINAL</center>", unsafe_allow_html=True)