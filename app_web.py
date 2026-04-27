import streamlit as st
import re, os, glob, PyPDF2, nltk
import pandas as pd
import plotly.express as px
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="VERIFIKASI-AI | By Fazrul", layout="wide")

# --- 2. ENGINE NLP (DENGAN CACHE) ---
@st.cache_resource
def load_nlp():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    except:
        pass
    return StemmerFactory().create_stemmer()

stemmer = load_nlp()

# Daftar Kata Buang (Stopwords) untuk akurasi tinggi
STOPWORDS_ID = set([
    'yang', 'untuk', 'pada', 'ke', 'para', 'namun', 'menurut', 'antara', 'dia', 'dua',
    'ia', 'seperti', 'jika', 'sehingga', 'kembali', 'dan', 'tidak', 'ini', 'karena',
    'kepada', 'oleh', 'saat', 'harus', 'sementara', 'setelah', 'belum', 'kami', 'sekitar',
    'bagi', 'serta', 'daripada', 'dengan', 'adalah', 'yaitu', 'yakni', 'itu', 'di'
])

def extract_pdf_text(file):
    text = ""
    try:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            res = page.extract_text()
            if res:
                text += res + " "
    except: pass
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    filtered_words = [w for w in words if w not in STOPWORDS_ID]
    text_clean = " ".join(filtered_words)
    if len(text_clean.split()) > 3:
        return stemmer.stem(text_clean)
    return text_clean

# --- 3. HEADER & IDENTITAS UTAMA ---
st.title("🛡️ VERIFIKASI-AI")
st.subheader("Sistem Deteksi Kemiripan Dokumen Berbasis Artificial Intelligence")
st.caption("Dikembangkan oleh: **Fazrul** | Versi 1.0 Global Scanner") 
st.markdown("---")

# --- 4. SIDEBAR (KONTROL & PROFIL PENGEMBANG) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.header("Sistem Audit")
    
    # Deteksi Database
    ref_files = glob.glob("database_lokal/*.pdf") + glob.glob("database_eksternal/*.pdf")
    
    if not ref_files:
        st.error("⚠️ Database Kosong!")
    else:
        st.success(f"📦 Database: {len(ref_files)} Dokumen")

    # --- IDENTITAS FAZRUL ---
    st.markdown("---")
    st.markdown("### 👨‍💻 Perancang Sistem")
    st.info("**Fazrul**")
    
    # Link Instagram Fazrul
    st.write("🔗 [Instagram Profil](https://www.instagram.com/fazrul_alexsander/)")
    st.link_button("Follow My Instagram", "https://www.instagram.com/fazrul_alexsander/")
    
    st.write("Project: Validasi Dokumen Akademik")
    st.write("Teknologi: Python AI & NLP")
    
    # Footer Copyright
    st.markdown("<br><br><p style='font-size: 0.8em; color: grey;'>© 2026 Fazrul. All Rights Reserved.</p>", unsafe_allow_html=True)

# --- 5. AREA KERJA ANALISIS ---
uploaded_file = st.file_uploader("Unggah Dokumen Uji (PDF)", type="pdf")

if uploaded_file and ref_files:
    if st.button("🔥 MULAI SCANNING CERDAS"):
        with st.status("AI Fazrul sedang bekerja...", expanded=True) as status:
            
            text_uji = extract_pdf_text(uploaded_file)
            kalimat_uji_raw = [s.strip() for s in nltk.sent_tokenize(text_uji) if len(s.split()) > 4]
            
            if not kalimat_uji_raw:
                st.error("Teks tidak terbaca.")
                st.stop()

            st.write("🔍 Memindai database referensi...")
            db_data = []
            for path_ref in ref_files:
                fname = os.path.basename(path_ref)
                with open(path_ref, 'rb') as f:
                    t_ref = extract_pdf_text(f)
                    k_ref = nltk.sent_tokenize(t_ref)
                    for s in k_ref:
                        if len(s.split()) > 4:
                            db_data.append({"sumber": fname, "clean": clean_text(s), "asli": s})

            st.write("🧠 Menghitung kemiripan makna...")
            match_counts = {os.path.basename(f): 0 for f in ref_files}
            hasil_plagiat = []

            for s_uji in kalimat_uji_raw:
                s_uji_clean = clean_text(s_uji)
                for item in db_data:
                    try:
                        vect = TfidfVectorizer().fit_transform([s_uji_clean, item['clean']])
                        sim = cosine_similarity(vect[0:1], vect[1:2])[0][0]
                        if sim > 0.80:
                            hasil_plagiat.append({"teks": s_uji, "sumber": item['sumber']})
                            match_counts[item['sumber']] += 1
                            break
                    except: continue
            
            status.update(label="Scanning Selesai!", state="complete")

        # --- 6. DISPLAY HASIL ---
        skor = (len(hasil_plagiat) / len(kalimat_uji_raw)) * 100 if kalimat_uji_raw else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("SKOR KEMIRIPAN", f"{skor:.1f}%")
        col2.metric("TEMUAN KALIMAT", len(hasil_plagiat))
        col3.metric("SUMBER AKTIF", len([v for v in match_counts.values() if v > 0]))

        st.divider()
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.subheader("📊 Statistik Sumber")
            df_grafik = pd.DataFrame(list(match_counts.items()), columns=['Dokumen', 'Kecocokan'])
            df_grafik = df_grafik[df_grafik['Kecocokan'] > 0]
            if not df_grafik.empty:
                fig = px.pie(df_grafik, values='Kecocokan', names='Dokumen', hole=.4)
                st.plotly_chart(fig, use_container_width=True)

        with c_right:
            st.subheader("📑 Detail Temuan")
            for h in hasil_plagiat[:10]:
                with st.expander(f"Sumber: {h['sumber']}"):
                    st.write(f"_{h['teks']}_")

        laporan = f"LAPORAN VERIFIKASI-AI\nPerancang: Fazrul\nFile: {uploaded_file.name}\nSkor: {skor:.1f}%"
        st.download_button("📩 Download Laporan", laporan, file_name=f"Laporan_Fazrul_{uploaded_file.name}.txt")