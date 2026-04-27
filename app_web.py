import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# Konfigurasi Halaman
st.set_page_config(page_title="Fazrul-PlagiaCheck Pro", layout="wide", page_icon="🛡️")

# Inisialisasi Sastrawi
@st.cache_resource
def get_stemmer():
    factory = StemmerFactory()
    return factory.create_stemmer()

stemmer = get_stemmer()

def bersihkan_teks(teks):
    teks = teks.lower()
    return stemmer.stem(teks)

def baca_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        teks = ""
        for page in reader.pages:
            teks += page.extract_text()
        return teks
    except:
        return ""

def ambil_teks_web(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ambil teks dari paragraf saja
        paragraphs = soup.find_all('p')
        return " ".join([p.get_text() for p in paragraphs])
    except:
        return "Error: Gagal mengambil data dari URL. Pastikan link benar."

def hitung_kemiripan(teks1, teks2):
    set1 = set(teks1.split())
    set2 = set(teks2.split())
    if not set1 or not set2: return 0
    irisan = set1.intersection(set2)
    return (len(irisan) / len(set1.union(set2))) * 100

# Tampilan UI
st.title("🛡️ FAZRUL PLAGIA-CHECK PRO V3.0")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Panel Kontrol")
    opsi = st.selectbox("Pilih Sumber Data:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    st.divider()
    st.write("📊 **Status Database:**")
    if os.path.exists("database_lokal"):
        jml = len([f for f in os.listdir("database_lokal") if f.endswith('.pdf')])
        st.success(f"{jml} Dokumen di Database")
    
    if st.button("Hapus Cache"):
        st.cache_resource.clear()
        st.rerun()

# Logika Input
teks_uji = ""
if opsi == "Upload PDF":
    file = st.file_uploader("Unggah file PDF", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif opsi == "Paste Teks AI":
    teks_uji = st.text_area("Tempel teks di sini:", height=250)
elif opsi == "Link Artikel Web":
    url = st.text_input("Masukkan URL Website (Contoh: https://berita.com/artikel)")
    if url:
        with st.spinner("Mengambil teks dari internet..."):
            teks_uji = ambil_teks_web(url)
            if "Error" in teks_uji:
                st.error(teks_uji)
                teks_uji = ""
            else:
                st.success("Teks berhasil ditarik!")

# Eksekusi Analisis
if st.button("🚀 JALANKAN ANALISIS SEKARANG"):
    if teks_uji:
        teks_uji_bersih = bersihkan_teks(teks_uji)
        folder_db = "database_lokal"
        hasil = []

        with st.spinner("Membandingkan dengan database..."):
            if os.path.exists(folder_db):
                for f_name in os.listdir(folder_db):
                    if f_name.endswith(".pdf"):
                        with open(os.path.join(folder_db, f_name), "rb") as f:
                            t_db = baca_pdf(f)
                            t_db_bersih = bersihkan_teks(t_db)
                            skor = hitung_kemiripan(teks_uji_bersih, t_db_bersih)
                            hasil.append((f_name, skor))

        # Tampilan Hasil
        st.subheader("📋 Hasil Verifikasi")
        if hasil:
            # Cari skor tertinggi
            hasil.sort(key=lambda x: x[1], reverse=True)
            top_file, top_skor = hasil[0]

            col1, col2, col3 = st.columns(3)
            col1.metric("Skor Tertinggi", f"{top_skor:.1f}%")
            col2.metric("Sumber Terdekat", top_file)
            col3.metric("Status", "⚠️ Plagiat" if top_skor > 30 else "✅ Aman")

            st.write("### Grafik Perbandingan:")
            for nama, skor in hasil:
                label = f"{nama} ({skor:.1f}%)"
                st.progress(skor/100)
                st.caption(label)
        else:
            st.warning("Tidak ada dokumen PDF di folder database_lokal untuk dibandingkan.")
    else:
        st.error("Masukkan data terlebih dahulu!")

st.markdown("---")
st.caption("© 2026 Fazrul Proyek - Update Berkala Aktif")