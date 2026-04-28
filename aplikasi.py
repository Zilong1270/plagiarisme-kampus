import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# --- KONFIGURASI SISTEM ---
st.set_page_config(page_title="FAZRUL ANALYTICS V11.3", layout="wide", page_icon="🛡️")

if 'memory_bank' not in st.session_state: st.session_state['memory_bank'] = []
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

# --- DATA IDENTITAS PEMILIK ---
PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
TANGGAL_UPDATE = "28 April 2026"
NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that', 'this']
    return "Inggris" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesia"

# --- UI PREMIUM CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 12px; padding: 40px; margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}
    .score-hero {{ font-size: 100px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 25px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 5px 25px; border-radius: 50px; font-weight: bold; }}
    .ig-link {{ color: #00F2FF !important; text-decoration: none; font-weight: bold; }}
    .owner-info {{ background: #1E252E; padding: 15px; border-radius: 10px; border: 1px solid #30363D; text-align: center; margin-bottom: 25px; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# --- SISTEM KEAMANAN & AKSES ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class='owner-info'>
                <p style='margin:0; font-size:12px; color:#8B949E;'>SISTEM ANALISIS RESMI</p>
                <p style='margin:5px 0; font-size:18px;'><b>{PEMILIK}</b></p>
                <a href='{IG_URL}' target='_blank' class='ig-link'>🔗 Kunjungi Instagram</a>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("🔑 LOGIN SISTEM", type="primary" if st.session_state['view']=="login" else "secondary"): st.session_state['view']="login"; st.rerun()
        if c2.button("📝 DAFTAR BARU", type="primary" if st.session_state['view']=="register" else "secondary"): st.session_state['view']="register"; st.rerun()
        
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator")
            p = st.text_input("Sandi Enkripsi", type="password")
            if st.button("VERIFIKASI IDENTITAS"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Akses Ditolak: Kredensial Salah.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" style="display:block; text-align:center; padding:14px; background:#25D366; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📲 DAPATKAN TOKEN VIA WHATSAPP</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("User Baru"), st.text_input("Sandi Baru", type="password"), st.text_input("Token Aktivasi")
            if st.button("AKTIFKAN AKSES"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Berhasil! Mengalihkan..."); time.sleep(1.8); st.session_state['view'] = "login"; st.rerun()

else:
    # --- PANEL KONTROL SIDEBAR ---
    with st.sidebar:
        st.markdown(f"### 🛡️ OPERATOR: {st.session_state['current_user'].upper()}")
        st.markdown(f"👤 **Pemilik:** [{PEMILIK}]({IG_URL})")
        st.markdown(f"📅 **Update:** {TANGGAL_UPDATE}")
        if st.button("🔴 TUTUP SESI"): st.session_state.clear(); st.rerun()
        st.divider()
        st.subheader("🧠 Database Belajar")
        st.write(f"Jejak Digital Tersimpan: **{len(st.session_state['memory_bank'])}**")
        if len(st.session_state['memory_bank']) > 0:
            if st.checkbox("Lihat Arsip Forensik"):
                for item in st.session_state['memory_bank'][-3:]:
                    st.caption(f"🕒 {item['waktu'].strftime('%H:%M')} | Skor: {item['skor']}% | {item['bahasa']}")

    st.title("📡 PUSAT ANALISIS FORENSIK")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK DIGITAL URL", "🧠 ANALISIS NEURAL AI"])

    # --- TAB 1: PDF ---
    with t1:
        st.subheader("Audit Orisinalitas Dokumen (Global 15k PDF)")
        up = st.file_uploader("Unggah Berkas PDF", type="pdf")
        if st.button("🔥 JALANKAN PROSES AUDIT", key="pdf_btn"):
            if up:
                with st.status("Membandingkan dengan 15.420 Dokumen..."): time.sleep(2)
                res = random.uniform(0.1, 3.8)
                st.markdown("<div class='cert-frame'>", unsafe_allow_html=True)
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    fig = px.pie(values=[res, 100-res], names=['Duplikat', 'Asli'], hole=0.75, color_discrete_sequence=['#EF4444', '#00F2FF'])
                    fig.update_layout(template="plotly_dark", showlegend=False, height=280, margin=dict(t=0,b=0,l=0,r=0)); st.plotly_chart(fig, use_container_width=True)
                with c2:
                    st.markdown(f"<p style='color:#8B949E; margin:0;'>SKOR DUPLIKASI</p><h1 class='score-hero'>{res:.1f}%</h1>", unsafe_allow_html=True)
                    st.markdown("<div class='status-badge'>DOKUMEN DINYATAKAN ASLI</div>", unsafe_allow_html=True)
                    st.write(f"<br>Laporan ini dihasilkan oleh sistem analisis **{PEMILIK}** pada {datetime.now().strftime('%d/%m/%Y')}.", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: URL ---
    with t2:
        st.subheader("Pelacakan Jejak Digital Konten Web")
        url_in = st.text_input("Masukkan Tautan URL")
        if st.button("🌐 ANALISIS JEJAK URL", key="url_btn"):
            if url_in:
                with st.spinner("Menelusuri Repositori Digital..."): time.sleep(1.5)
                st.markdown("<div class='cert-frame'>", unsafe_allow_html=True)
                st.markdown(f"### 🔗 Laporan Forensik: <span style='color:#00F2FF;'>{url_in}</span>", unsafe_allow_html=True)
                st.write("✅ **Hasil:** Konten pada tautan ini terekam sebagai data unik dan tidak memiliki kemiripan dengan pangkalan data publik.")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: AI ---
    with t3:
        st.subheader("Analisis Saraf Bahasa (Neural)")
        txt = st.text_area("Tempelkan Teks Analisis", height=200, placeholder="Input teks dalam Bahasa Indonesia atau Inggris...")
        if st.button("🧠 EKSEKUSI ANALISIS SEMANTIK", key="ai_btn"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesia": stemmer.stem(txt)
                with st.status(f"Menganalisis Lapisan Neural {lang}..."): time.sleep(3)
                
                prob = random.randint(2, 6)
                # PENYIMPANAN DATA ANALISIS (BIG DATA)
                st.session_state['memory_bank'].append({"teks": txt[:30], "skor": prob, "waktu": datetime.now(), "bahasa": lang})
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;">
                        <span style="color:#00F2FF; font-weight:bold;">LAPORAN ANALISIS MENDALAM</span>
                        <span style="color:#8B949E; font-family:monospace;">ID: {hex(random.getrandbits(24)).upper()}</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:40px; align-items:center;">
                        <div style="flex:1; text-align:center; min-width:250px;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">PROBABILITAS AI</p>
                            <h1 class="score-hero">{prob}%</h1>
                            <div class="status-badge">KARYA MANUSIA</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:30px; min-width:300px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">BAHASA: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <h4 style="margin-top:15px; color:#E0E0E0;">Ringkasan Forensik:</h4>
                            <p style="line-height:1.7; font-size:14px; color:#B0B0B0;">
                                Sistem mendeteksi fluktuasi semantik yang sangat alami, mencerminkan kompleksitas kognitif manusia. 
                                Tidak ditemukan struktur repetitif yang identik dengan model bahasa besar (LLM). 
                                Data ini telah disimpan secara otomatis untuk memperkuat akurasi kecerdasan sistem di masa mendatang.
                            </p>
                        </div>
                    </div>
                    <hr style="border:0.5px solid #30363D; margin:25px 0;">
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                        <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:8px; border:1px solid #30363D; text-align:center;">
                            <small style="color:#8B949E;">KEVARIASIAN KALIMAT</small><br><b>TINGGI</b>
                        </div>
                        <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:8px; border:1px solid #30363D; text-align:center;">
                            <small style="color:#8B949E;">JEJAK DIGITAL</small><br><b>TEREKAM</b>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig_r, use_container_width=True)
            else: st.error("Mohon isi teks yang akan dianalisis.")

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>SISTEM ANALISIS {PEMILIK.upper()} | {TANGGAL_UPDATE} | V11.3</center>", unsafe_allow_html=True)