import streamlit as st
import base64

def apply_custom_css():
    """Fungsi styling dasar untuk komponen kustom HTML"""
    st.markdown("""
    <style>
        /* Styling Elemen Chatbot Header di Kolom Kanan */
        .chat-header {
            background-color: #1E3A8A;
            color: white;
            padding: 14px;
            border-radius: 12px 12px 0 0;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: -5px;
        }
        .status-dot {
            width: 10px;
            height: 10px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero_section():
    """Fungsi untuk menampilkan banner utama/hero section dengan Logo DKI"""
    try:
        with open("assets/logo_dki.jpeg", "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        logo_url = f"data:image/jpeg;base64,{encoded_logo}"
    except Exception:
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Logo_DKI_Jakarta.svg"

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); padding: 40px; border-radius: 24px; color: white; margin-bottom: 30px; display: flex; align-items: center; gap: 30px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);">
        <img src="{logo_url}" width="100" style="object-fit: contain; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.2));">
        <div>
            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;">Dinas Kependudukan dan Pencatatan Sipil</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-size: 16px; opacity: 0.9;">Provinsi DKI Jakarta — Melayani dengan Profesional, Transparan, dan Akuntabel</p>
        </div>
    </div>
    """, unsafe_allow_html=True)