import streamlit as st
st.set_page_config(page_title='Fazrul Anti-Plagiat', page_icon='🛡️')
st.title('🛡️ Fazrul Plagiarism Checker V3.8')
st.write('Selamat datang, silakan unggah dokumen untuk diperiksa.')
uploaded_file = st.file_uploader('Pilih file PDF...', type='pdf')
if uploaded_file is not None:
    st.success('File berhasil diunggah! Sedang menganalisis...')
st.divider()
st.caption('© 2026 Dibuat oleh Fazrul Alexander')
