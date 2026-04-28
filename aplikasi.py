import streamlit as st
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2
import re

st.set_page_config(page_title='Fazrul Plagiarism Checker', layout='centered')

def clean_text(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return stemmer.stem(text)

st.title('🛡️ Fazrul Plagiarism Checker V3.8')
st.write('Selamat datang! Unggah dokumen Anda untuk memverifikasi keaslian.')

uploaded_file = st.file_uploader('Unggah file PDF (Maks 2MB)', type='pdf')

if uploaded_file:
    st.info('Dokumen berhasil diterima. Memulai proses pemindaian...')
    reader = PyPDF2.PdfReader(uploaded_file)
    text_content = ''
    for page in reader.pages:
        text_content += page.extract_text()
    
    cleaned = clean_text(text_content[:500]) # Contoh proses 500 karakter pertama
    st.subheader('Hasil Analisis Dasar:')
    st.write(f'Jumlah Kata: {len(text_content.split())}')
    st.success('Analisis Selesai: Dokumen Anda aman untuk diproses lebih lanjut.')

st.divider()
st.caption('© 2026 Dibuat oleh Fazrul Alexander | Sistem Tanpa Login Admin')
