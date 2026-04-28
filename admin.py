import streamlit as st
import os

st.set_page_config(page_title="Admin Monitoring", page_icon="🔐")

pass_admin = st.sidebar.text_input("Password Master", type="password")

if pass_admin == "fazruladmin2026":
    st.title("📊 Monitoring Jejak Digital")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🕵️ Log Aktivitas (Real-time)")
        if os.path.exists("log_akses.txt"):
            with open("log_akses.txt", "r") as f:
                logs = f.readlines()
            st.text_area("Aktivitas Terbaru:", value="".join(logs[::-1]), height=400)
            
    with col2:
        st.subheader("👥 Daftar Anggota")
        if os.path.exists("users_data.txt"):
            with open("users_data.txt", "r") as f:
                users = f.readlines()
            for u in users:
                st.write(f"✅ {u.strip()}")
        else:
            st.write("Belum ada user yang daftar.")

else:
    st.warning("Masukkan Password Master untuk melihat Jejak Digital.")
