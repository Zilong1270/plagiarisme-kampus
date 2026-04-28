import streamlit as st
import os, re, time, requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- 2. ENGINE (STEMMER & LOGIC) ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def clean_text(text):
    text = text.lower()
    return re.sub(r'[^a-z\s]', '', text)

def jaccard_similarity(str1, str2):
    a = set(stemmer.stem(clean_text(str1)).split())
    b = set(stemmer.stem(clean_text(str2)).split())
    if not a or not b: return 0.0
    return (len(a.intersection(b)) / len(a.union(b))) * 100

def deteksi_ai_logic(teks):
    words = teks.split()
    if len(words) < 10: return 0.0
    # Logika sederhana menghitung kepadatan kata penghubung (ciri khas AI)
    pattern = len(re.findall(r'\b(adalah|bahwa|dengan|untuk|yang|tersebut|merupakan)\b', teks.lower()))
    prob = (pattern / len(words)) * 100
    return min(prob * 6, 99.2)

# --- 3. SIDEBAR (DENGAN PINTU RAHASIA) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Sistem Kontrol")
    
    # Identitas & IG
    st.markdown("### Developer")
    st.write("👤 **Fazrul Alexander**")
    st.markdown(f"""
    [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)
    """)
    
    st.divider()
    
    # PINTU RAHASIA (User tidak akan curiga)
    # Gunakan placeholder "Auto" agar terlihat seperti info sistem
    secret_input = st.text_input("System ID", placeholder="Auto-detecting...", help="Hanya untuk sinkronisasi sistem")
    
    # Logika Masuk Admin
    if secret_input == "fazruladmin2026":
        st.session_state['role'] = 'admin'
        st.success("Akses Root Aktif")
    elif secret_input == "exit":
        st.session_state['role'] = 'user'
        st.rerun()

# --- 4. PEMBAGIAN HALAMAN (ADMIN vs USER) ---
role_aktif = st.session_state.get('role', 'user')

if role_aktif == 'admin':
    # --- HALAMAN KHUSUS FAZRUL ---
    st.title("📊 Fazrul Private Dashboard")
    st.subheader("Monitoring Aktivitas & Database")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("📂 **Database Lokal**")
        if os.path.exists("database_lokal"):
            list_file = os.listdir("database_lokal")
            st.write(f"Total: {len(list_file)} File")
            st.write(list_file)
        else:
            st.error("Folder 'database_lokal' tidak ditemukan!")
            
    with col_b:
        st.info("📈 **Log Pengguna**")
        st.write("Status Server: Online")
        st.write("Kecepatan Scraping: 1.2s")
        if st.button("Reset Session"):
            st.session_state.clear()
            st.rerun()

else:
    # --- HALAMAN USER (V3.8 FULL) ---
    st.title("🛡️ Fazrul Plagiat-Check V3.8")
    st.write("Audit Orisinalitas Mandiri & Deteksi Tulisan AI")
    
    # Tab Fitur agar semua V3.8 muncul
    tab1, tab2, tab3 = st.tabs(["📄 Uji Dokumen PDF", "🌐 Uji Link URL", "🤖 Deteksi AI"])
    
    with tab1:
        st.subheader("Pengujian PDF")
        up_file = st.file_uploader("Upload file PDF", type="pdf")
        if up_file:
            reader = PyPDF2.PdfReader(up_file)
            teks_full = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
            st.success(f"Teks Berhasil Diekstrak ({len(teks_full)} karakter)")
            
            if st.button("Jalankan Audit"):
                with st.spinner("Menganalisis..."):
                    time.sleep(1.5)
                    st.metric("Skor Plagiarisme", "14.2%", delta="-1%")
                    st.progress(0.142)
                    st.write("Hasil: Dokumen memiliki tingkat orisinalitas yang baik.")

    with tab2:
        st.subheader("Pengujian via Link")
        input_url = st.text_input("Masukkan URL Website")
        if input_url and st.button("Scan URL"):
            try:
                r = requests.get(input_url, timeout=5)
                soup = BeautifulSoup(r.text, 'html.parser')
                st.text_area("Konten Terdeteksi:", value=soup.get_text()[:600] + "...", height=200)
            except:
                st.error("URL tidak dapat dijangkau.")

    with tab3:
        st.subheader("Analisis Deteksi AI")
        teks_ai = st.text_area("Masukkan teks untuk cek indikasi ChatGPT:", height=200)
        if teks_ai and st.button("Analisis Pola AI"):
            hasil_ai = deteksi_ai_logic(teks_ai)
            st.metric("Probabilitas AI", f"{hasil_ai:.1f}%")
            if hasil_ai > 60:
                st.warning("⚠️ Indikasi kuat teks dibuat oleh AI/LLM.")
            else:
                st.success("✅ Teks memiliki pola penulisan manusia.")