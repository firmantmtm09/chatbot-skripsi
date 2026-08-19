import streamlit as st
import base64

def apply_custom_css():
    st.markdown("""
    <style>
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

        .hero-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            padding: 35px 40px;
            border-radius: 24px;
            color: white;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 30px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
        }

        @media only screen and (max-width: 768px) {
            .block-container {
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
                padding-top: 1rem !important;
            }

            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                margin-bottom: 15px;
            }

            .hero-banner {
                flex-direction: column !important;
                text-align: center !important;
                padding: 24px 16px !important;
                gap: 15px !important;
                border-radius: 16px !important;
            }

            .hero-banner img {
                width: 70px !important;
            }

            .hero-banner h1 {
                font-size: 20px !important;
                line-height: 1.3 !important;
            }

            .hero-banner p {
                font-size: 13px !important;
            }

            div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_hero_section():
    try:
        with open("assets/logo_dki.jpeg", "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        logo_url = f"data:image/jpeg;base64,{encoded_logo}"
    except Exception:
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/b/b9/Logo_DKI_Jakarta.svg"

    st.markdown(f"""
    <div class="hero-banner">
        <img src="{logo_url}" width="100" style="object-fit: contain; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.2));">
        <div>
            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;">Dinas Kependudukan dan Pencatatan Sipil</h1>
            <p style="color: #cbd5e1; margin: 5px 0 0 0; font-size: 16px; opacity: 0.9;">Provinsi DKI Jakarta — Melayani dengan Profesional, Transparan, dan Akuntabel</p>
        </div>
    </div>
    """, unsafe_allow_html=True)