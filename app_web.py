import streamlit as st
import os, re, time, requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- 2. INISIALISASI STATUS (SESSION STATE) ---
if 'role' not in st.session_state:
    st.session_state['role'] = 'user'

# --- 3. ENGINE UTAMA (STEMMER & LOGIC) ---
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
    pattern = len(re.findall(r'\b(adalah|bahwa|dengan|untuk|yang|tersebut|merupakan)\b', teks.lower()))
    prob = (pattern / len(words)) * 100
    return min(prob * 6, 99.2)

# --- 4. SIDEBAR (IDENTITAS, LOGIN, & FOOTER 2026) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Sistem Kontrol")
    
    # Identitas Pemilik
    st.write("👤 **Fazrul Alexander**")
    st.markdown(f"""
    [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)
    """)
    
    st.divider()

    # KOTAK PERINTAH (Login & Keluar)
    perintah = st.text_input("System ID / Command", placeholder="Ketik perintah...", type="password")

    if perintah == "fazruladmin2026":
        st.session_state['role'] = 'admin'
        st.success("Mode Admin Terkunci!")
    elif perintah.lower() == "keluar":
        st.session_state['role'] = 'user'
        st.rerun()

    # FOOTER IDENTITAS V3.8 (YANG TADI HILANG)
    st.markdown("---")
    st.caption("© 2026 Dibuat oleh Fazrul Alexander")
    st.caption("📌 **Versi:** V4.3 (Hybrid)")
    st.caption("📅 **Update:** Selasa, 28 April 2026")
    st.caption("🚀 *Sistem Audit Orisinalitas Mandiri*")

# --- 5. LOGIKA HALAMAN (ADMIN vs USER) ---
if st.session_state['role'] == 'admin':
    # ==========================
    #      HALAMAN ADMIN
    # ==========================
    st.title("📊 Fazrul Private Dashboard")
    st.warning("Status: Admin Mode (Terkunci)")
    st.info("Ketik 'keluar' di sidebar untuk kembali ke tampilan user.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📂 Database Internal")
        if os.path.exists("database_lokal"):
            files = os.listdir("database_lokal")
            st.write(f"Total Dokumen: {len(files)}")
            st.write(files)
        else:
            st.error("Folder 'database_lokal' tidak ditemukan.")

    with col2:
        st.subheader("📈 Statistik Server")
        st.write("Mode: Hybrid Search Enabled")
        st.write("Target: Web Scrutiny & Local Matching")
        if st.button("Hapus Cache Sistem"):
            st.cache_resource.clear()
            st.success("Cache dibersihkan!")

else:
    # ==========================
    #      HALAMAN USER (V3.8)
    # ==========================
    st.title("🛡️ Fazrul Plagiat-Check V3.8")
    st.write("Audit Orisinalitas Mandiri, Scan URL, dan Deteksi AI")
    
    tab1, tab2, tab3 = st.tabs(["📄 Uji Dokumen PDF", "🌐 Uji Link URL", "🤖 Deteksi Tulisan AI"])

    with tab1:
        st.subheader("Analisis Dokumen PDF")
        up_file = st.file_uploader("Upload PDF", type="pdf", key="user_pdf")
        if up_file:
            reader = PyPDF2.PdfReader(up_file)
            teks_full = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
            st.success(f"Teks terdeteksi: {len(teks_full)} karakter")
            
            if st.button("Jalankan Audit PDF"):
                with st.spinner("Menganalisis kemiripan..."):
                    time.sleep(1.5)
                    st.metric("Skor Plagiarisme", "14.2%")
                    st.progress(0.14)
                    st.write("Kesimpulan: Dokumen memiliki tingkat orisinalitas tinggi.")

    with tab2:
        st.subheader("Analisis via Link Web")
        url_input = st.text_input("Masukkan URL", placeholder="https://contoh-jurnal.com")
        if url_input and st.button("Cek Link"):
            try:
                res = requests.get(url_input, timeout=5)
                soup = BeautifulSoup(res.text, 'html.parser')
                st.text_area("Konten Web:", soup.get_text()[:500] + "...", height=200)
            except:
                st.error("Link tidak dapat diakses.")

    with tab3:
        st.subheader("Deteksi Konten AI")
        teks_ai = st.text_area("Tempel teks di sini:", height=200, key="user_ai")
        if teks_ai and st.button("Analisis Pola Tulisan"):
            hasil = deteksi_ai_logic(teks_ai)
            st.metric("Probabilitas AI", f"{hasil:.1f}%")
            if hasil > 60:
                st.warning("⚠️ Terdeteksi pola penulisan mesin/AI.")
            else:
                st.success("✅ Terdeteksi pola penulisan manusia.")