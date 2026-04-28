import streamlit as st
import os

st.set_page_config(page_title="Admin Panel Fazrul", page_icon="🔐")

# --- LOGIN SEDERHANA ---
password = st.sidebar.text_input("Masukkan Password Admin", type="password")

if password == "fazruladmin2026":
    st.title("📊 Dashboard Admin Fazrul")
    st.success("Akses Diterima! Selamat bekerja, Fazrul.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📁 File di Server")
        if os.path.exists("."):
            files = os.listdir(".")
            st.write(files)
            
    with col2:
        st.subheader("⚙️ Status Sistem")
        st.write("Database: Terhubung")
        st.write("Versi Server: 2026.04")
else:
    st.title("🔐 Akses Terbatas")
    st.warning("Silakan masukkan password di sidebar untuk membuka dashboard.")
