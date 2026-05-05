import streamlit as st
import os
import time
import re
import spacy
from datetime import datetime

# --- SETUP MODEL & API ---
os.environ["GROQ_API_KEY"] = "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"

# Load spaCy untuk analisis skripsi (NER)
try:
    nlp = spacy.load("xx_ent_wiki_sm")
except:
    os.system("python -m spacy download xx_ent_wiki_sm")
    nlp = spacy.load("xx_ent_wiki_sm")

st.set_page_config(page_title="Asisten Dukcapil", page_icon="🏛️", layout="centered")

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.llm = Groq(model="llama-3.1-8b-instant")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI CUSTOM CSS (Versi Favorit Lo) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
*, html, body { font-family: 'Inter', sans-serif !important; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"], .stApp,
[data-testid="stMain"], [data-testid="stMainBlockContainer"],
div[class*="block-container"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

[data-testid="stHeader"] { background-color: #ffffff !important; }

[data-testid="stBottom"], [data-testid="stBottomBlockContainer"], 
[class*="stChatInputContainer"] {
    background-color: #ffffff !important;
}

[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e5e7eb !important;
}

[data-testid="stChatInput"] {
    background-color: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 14px !important;
}

[data-testid="stChatMessage"] {
    background-color: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 16px !important;
}

.jam-buka { background: #dcfce7; color: #15803d; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }
.jam-tutup { background: #fee2e2; color: #dc2626; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; }

#MainMenu, footer, header { display: none !important; visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# --- FUNGSI PROSES DATA ---
@st.cache_resource(show_spinner="Memuat dokumen...")
def prepare_data():
    reader = SimpleDirectoryReader(input_dir="./Data")
    raw_docs = reader.load_data()
    clean_docs = []
    for doc in raw_docs:
        # PERBAIKAN: Spasi dijaga agar teks terbaca normal
        clean_text = re.sub(r'\s+', ' ', doc.text).strip()
        clean_docs.append(Document(text=clean_text))
    index = VectorStoreIndex.from_documents(clean_docs)
    return index, len(raw_docs)

def extract_ner(text):
    doc = nlp(text)
    return [f"{ent.text} ({ent.label_})" for ent in doc.ents]

# --- SIDEBAR (Persis seperti tampilan awal lo) ---
try:
    with st.sidebar:
        st.markdown("""
            <div style='text-align:center;'>
                <img src='https://cdn-icons-png.flaticon.com/512/5962/5962463.png' width='75'>
                <h3 style='color:#111827; margin:8px 0 2px;'>Asisten Dukcapil</h3>
                <p style='color:#6b7280; font-size:0.82em; margin:0;'>Layanan Informasi Warga</p>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        index, doc_count = prepare_data()

        st.markdown(f"""
            <div style='background:#eff6ff; border:1px solid #3b82f6;
                border-radius:10px; padding:10px 12px; margin-bottom:8px;'>
                <span style='color:#3b82f6; font-size:12px; font-weight:600;'>
                    📄 {doc_count} halaman dokumen ter-load
                </span>
            </div>
        """, unsafe_allow_html=True)

        st.success("✅ Database Terintegrasi")
        st.warning("💡 Seluruh layanan administrasi adalah **GRATIS**.")
        st.divider()

        # Status Operasional
        now = datetime.now()
        is_open = now.weekday() < 5 and 8 <= now.hour < 15
        status_html = '<span class="jam-buka">🟢 Sedang Buka</span>' if is_open else '<span class="jam-tutup">🔴 Sedang Tutup</span>'
        st.markdown(f"""
            <div style='margin-bottom:12px;'>
                <b style='color:#111827; font-size:13px;'>🕐 Jam Operasional</b><br>
                <span style='color:#6b7280; font-size:12px;'>Senin–Jumat, 08.00–15.00 WIB</span><br>
                <div style='margin-top:6px;'>{status_html}</div>
            </div>
        """, unsafe_allow_html=True)

        st.divider()
        # Link Terkait
        st.markdown("<b style='color:#111827; font-size:13px;'>🔗 Link Terkait</b>", unsafe_allow_html=True)
        st.caption("[Portal Alpukat Betawi](https://alpukat-dukcapil.jakarta.go.id/)")
        st.caption("[Panduan Layanan Online](https://alpukat-dukcapil.jakarta.go.id/panduan)")
        st.divider()

        if st.button("🗑️ Hapus Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # --- CHAT ENGINE ---
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt="""Kamu adalah asisten Dukcapil DKI Jakarta yang ramah. 
        PENTING: Gunakan format markdown bullet points (-) untuk daftar persyaratan. 
        Jawab HANYA berdasarkan dokumen."""
    )

    # --- TAMPILAN AWAL (Hero Section) ---
    if not st.session_state.messages:
        st.markdown("<div style='text-align:center; font-size:3.5rem; margin-top:1.5rem;'>🏛️</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:#111827; font-weight:800; font-size:2.4rem; text-align:center;'>Pusat Informasi Digital</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6b7280; text-align:center; margin-bottom:2rem;'>Syarat dokumen & layanan Dukcapil DKI Jakarta.</p>", unsafe_allow_html=True)

        _, center, _ = st.columns([1, 2, 1])
        with center:
            c1, c2 = st.columns(2)
            if c1.button("🏠 Syarat KK", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Apa syarat membuat Kartu Keluarga baru?"})
                st.rerun()
            if c2.button("🪪 Urusan KTP", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Bagaimana prosedur dan syarat membuat KTP elektronik?"})
                st.rerun()

    # --- LOGIKA CHAT ---
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "entities" in msg and msg["entities"]:
                 st.caption(f"🔍 Entitas terdeteksi: {', '.join(msg['entities'])}")

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        user_input = st.session_state.messages[-1]["content"]
        detected_entities = extract_ner(user_input)
        st.session_state.messages[-1]["entities"] = detected_entities

        with st.chat_message("assistant"):
            with st.spinner("Mencari informasi..."):
                response = chat_engine.chat(user_input)
                
                # Merapikan output nomor menjadi baris baru
                formatted_text = response.response.replace(". 1.", ".\n\n- ").replace(". 2.", ".\n\n- ").replace(". 3.", ".\n\n- ").replace(". 4.", ".\n\n- ").replace(". 5.", ".\n\n- ")
                
                placeholder = st.empty()
                full_response = ""
                for chunk in formatted_text.split():
                    full_response += chunk + " "
                    time.sleep(0.01)
                    placeholder.markdown(full_response + "▌")
                
                final = f"{full_response.strip()}\n\n---\n*📄 Sumber: Dokumen Resmi Dukcapil DKI Jakarta*"
                placeholder.markdown(final)
                st.session_state.messages.append({"role": "assistant", "content": final})

    if prompt := st.chat_input("Ada yang bisa kami bantu hari ini?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

except Exception as e:
    st.error(f"⚠️ Terjadi kendala teknis: {e}")