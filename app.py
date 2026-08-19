import os
import streamlit as st
from frontend.styles import apply_custom_css, render_hero_section
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.llms.groq import Groq

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Portal Resmi Dukcapil DKI Jakarta",
    page_icon="🏛️",
    layout="wide"
)

apply_custom_css()

# Memuat environment variables lokal (jika ada)
load_dotenv()

# Mengambil API Key dari Streamlit Secrets (untuk cloud) atau .env (untuk lokal)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Inisialisasi RAG LlamaIndex & Groq (Dicache agar tidak memuat ulang terus menerus)
@st.cache_resource
def init_rag_system():
    try:
        llm = Groq(model="openai/gpt-oss-20b", api_key=GROQ_API_KEY, temperature=0, max_tokens=1500)
        Settings.llm = llm
        Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        Settings.text_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=30)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.abspath(os.path.join(BASE_DIR, "Data"))
        
        if not os.path.exists(data_path):
            data_path = os.path.join(BASE_DIR, "Data")
            
        print(f"Memuat dokumen dari direktori: {data_path}")
        documents = SimpleDirectoryReader(data_path).load_data()
        index = VectorStoreIndex.from_documents(documents)
        
        system_prompt = (
            "Kamu adalah asisten virtual resmi Dukcapil DKI Jakarta. "
            "Jawablah pertanyaan berdasarkan informasi yang akurat dari context yang diberikan. "
            "Jangan mengurangi atau mengubah angka, syarat, atau ketentuan spesifik yang ada di dalam dokumen. "
            "Gunakan format bullet points dan awali dengan sapaan ramah.\n\n"
            "Context:\n{context_str}\n\n"
            "Pertanyaan: {query_str}\n"
            "Jawaban:"
        )
        
        template = PromptTemplate(system_prompt)
        engine = index.as_query_engine(text_qa_template=template, similarity_top_k=6)
        print("Sistem RAG berhasil diinisialisasi.")
        return engine
    except Exception as e:
        print(f"Error inisialisasi sistem: {e}")
        return None

query_engine = init_rag_system()

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
</style>
""", unsafe_allow_html=True)

render_hero_section()

col_portal_kiri, col_chatbot_kanan = st.columns([0.73, 0.27], gap="large")

with col_portal_kiri:
    menu_tabs = ["Beranda", "Profil", "Layanan Online", "Regulasi & Informasi", "Kontak Kami"]
    selected_tab = st.tabs(menu_tabs)

    with selected_tab[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("###  Akses Layanan & Informasi")
        
        st.markdown("""
        <style>
            .grid-container-responsive {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
                width: 100%;
                margin-bottom: 25px;
                box-sizing: border-box;
            }
            .card-link {
                text-decoration: none !important;
                display: block;
            }
            .custom-card {
                border-radius: 16px;
                padding: 20px 10px;
                text-align: center;
                min-height: 140px;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                box-sizing: border-box;
            }
            .custom-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 18px -4px rgba(0,0,0,0.08);
                cursor: pointer;
            }
            .card-alpukat { background-color: #FFFBEB; border: 1px solid #FDE68A; color: #92400E !important; }
            .card-spm { background-color: #EFF6FF; border: 1px solid #BFDBFE; color: #1E40AF !important; }
            .card-berita { background-color: #F0FDF4; border: 1px solid #BBF7D0; color: #166534 !important; }
            .card-statistik { background-color: #FDF2F8; border: 1px solid #FBCFE8; color: #9D174D !important; }
            .card-icon { font-size: 24px; margin-bottom: 6px; }
            .card-title { font-size: 13px; font-weight: 700; margin-bottom: 4px; line-height: 1.3; }
            .card-desc { font-size: 11px; opacity: 0.85; line-height: 1.3; }
        </style>
        """, unsafe_allow_html=True)

        query_params = st.query_params
        current_menu = query_params.get("menu", None)

        st.markdown("""
        <div class="grid-container-responsive">
            <a href="https://alpukat-dukcapil.jakarta.go.id/?menu=alpukat" target="_self" class="card-link">
                <div class="custom-card card-alpukat">
                    <div class="card-icon">🥑</div>
                    <div class="card-title">Alpukat Betawi</div>
                    <div class="card-desc">Akses Langsung Pelayanan Dokumen Cepat & Akurat</div>
                </div>
            </a>
            <a href="/?menu=spm" target="_self" class="card-link">
                <div class="custom-card card-spm">
                    <div class="card-icon">📋</div>
                    <div class="card-title">Standar Pelayanan</div>
                    <div class="card-desc">Persyaratan & Prosedur SPM Kecamatan & Kelurahan</div>
                </div>
            </a>
            <a href="/?menu=berita" target="_self" class="card-link">
                <div class="custom-card card-berita">
                    <div class="card-icon">📰</div>
                    <div class="card-title">Berita Dukcapil</div>
                    <div class="card-desc">Informasi Terkini Seputar Kegiatan Kependudukan</div>
                </div>
            </a>
            <a href="/?menu=statistik" target="_self" class="card-link">
                <div class="custom-card card-statistik">
                    <div class="card-icon">📊</div>
                    <div class="card-title">Statistik Kependudukan</div>
                    <div class="card-desc">Grafik Konsolidasi Bersih Penduduk Provinsi DKI</div>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if current_menu == "alpukat":
            st.markdown("""
            <div style="background-color: #FFFBEB; padding: 24px; border-radius: 16px; border-left: 5px solid #F59E0B; margin-bottom: 25px;">
                <h4 style="color: #92400E; margin-top:0; font-weight:700;">🥑 Layanan Integrasi Alpukat Betawi</h4>
                <p style="color: #B45309; font-size:14px; line-height:1.6;">Akses langsung untuk memproses permohonan dokumen administrasi kependudukan Anda secara mandiri.</p>
                <a href="https://alpukat-dukcapil.jakarta.go.id/" target="_blank" style="background: #F59E0B; color:white; padding: 10px 20px; border-radius:10px; text-decoration:none; display:inline-block; font-weight:600; font-size:13px;">Masuk ke Aplikasi →</a>
            </div>
            """, unsafe_allow_html=True)
        elif current_menu == "spm":
            st.markdown("""
            <div style="background-color: #EFF6FF; padding: 24px; border-radius: 16px; border-left: 5px solid #3B82F6; margin-bottom: 25px;">
                <h4 style="color: #1E40AF; margin-top:0; font-weight:700;">📋 Standar Pelayanan Minimal (SPM) DKI Jakarta</h4>
                <p style="color: #1D4ED8; font-size:14px; line-height:1.6;">Komitmen loket pelayanan adminduk:</p>
                <ul style="color: #1D4ED8; font-size:14px; line-height:1.6; padding-left:20px;">
                    <li>Penerbitan Kartu Keluarga (KK) selesai maksimal dalam <b>1 hari kerja</b>.</li>
                    <li>Perekaman dan cetak KTP-el baru selesai dalam waktu <b>24 jam</b> sejak status tunggal pusat.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        elif current_menu == "berita":
            st.markdown("""
            <div style="background-color: #F0FDF4; padding: 24px; border-radius: 16px; border-left: 5px solid #10B981; margin-bottom: 25px;">
                <h4 style="color: #166534; margin-top:0; font-weight:700;">📰 Berita Terkini & Agenda Dinas</h4>
                <p style="color: #15803D; font-size:14px; line-height:1.6;"><b>Digital ID:</b> Aktivasi Identitas Kependudukan Digital (IKD) kini bisa dilakukan serentak di gerai Dukcapil terdekat.</p>
            </div>
            """, unsafe_allow_html=True)
        elif current_menu == "statistik" or current_menu is None:
            st.markdown("""
            <div style="background-color: #FDF2F8; padding: 24px; border-radius: 16px; border-left: 5px solid #EC4899; margin-bottom: 25px;">
                <h4 style="color: #9D174D; margin-top:0; font-weight:700;">📊 Statistik Konsolidasi Penduduk Bersih</h4>
                <p style="color: #BE185D; font-size:14px; line-height:1.6;">Data agregat berkala menunjukkan total penduduk Provinsi DKI Jakarta tercatat stabil dan presisi.</p>
            </div>
            """, unsafe_allow_html=True)

    with selected_tab[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        sub_menu_profil = st.selectbox(
            "Pilih Kategori Informasi Profil:",
            ["Tugas dan Fungsi", "Struktur Organisasi", "Profil Kepala Dinas", "Profil Pejabat", "Sejarah"],
            index=0
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if sub_menu_profil == "Tugas dan Fungsi":
            st.markdown("#### 🎯 Kedudukan, Tugas, and Fungsi")
            st.write("""
            Berdasarkan **Peraturan Gubernur Provinsi Daerah Khusus Ibukota Jakarta Nomor 57 Tahun 2022** tentang Organisasi Dan Tata Kerja Perangkat Daerah mempunyai tugas menyelenggarakan urusan pemerintahan bidang administrasi kependudukan dan pencatatan sipil.
            """)
        elif sub_menu_profil == "Struktur Organisasi":
            st.markdown("#### 🏢 Struktur Organisasi")
            try:
                st.image("assets/struktur_organisasi.jpeg", caption="Bagan Organisasi Disdukcapil DKI Jakarta", use_container_width=True)
            except Exception as e:
                st.error(f"Gagal memuat gambar struktur organisasi: {e}")
        elif sub_menu_profil == "Profil Kepala Dinas":
            st.markdown("#### 👤 Profil Kepala Dinas")
            col_foto, col_biodata = st.columns([0.3, 0.7], gap="large")
            with col_foto:
                try:
                    st.image("assets/kepala_dinas.jpeg", caption="DENNY WAHYU HARYANTO", use_container_width=True)
                except Exception as e:
                    st.error(f"Gagal memuat gambar kepala dinas: {e}")
            with col_biodata:
                st.markdown("##### **DENNY WAHYU HARYANTO**")
                st.write("Kepala Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta.")
        elif sub_menu_profil == "Profil Pejabat":
            st.markdown("#### 👥 Profil Pejabat Struktural")
            st.write("Daftar Pemangku Jabatan Struktural Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta.")
        elif sub_menu_profil == "Sejarah":
            st.markdown("#### 📜 Sejarah Singkat")
            st.write("Sejarah perkembangan layanan Dukcapil dari masa kolonial hingga era digital.")

    with selected_tab[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌐 Sistem Layanan Online Masyarakat")
        st.write("Silakan pilih ekosistem aplikasi resmi Disdukcapil DKI Jakarta.")

    with selected_tab[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚖️ Dasar Hukum & Regulasi Adminduk")
        with st.expander("📄 UU Nomor 24 Tahun 2013 tentang Administrasi Kependudukan"):
            st.write("Undang-Undang yang mengatur pengurusan dokumen kependudukan gratis dan KTP seumur hidup.")

    with selected_tab[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📞 Hubungi Kami")
        st.write("Dinas Kependudukan dan Pencatatan Sipil DKI Jakarta - Jl. Letjen S. Parman No.7.")

with col_chatbot_kanan:
    st.markdown("""
    <div class="chat-header">
        <div class="status-dot"></div>
        🏛️ ASISTEN VIRTUAL DUKCAPIL
    </div>
    """, unsafe_allow_html=True)

    chat_container = st.container(height=500)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Selamat datang di Portal Dukcapil Jakarta. Ada yang bisa saya bantu hari ini?"}]

    with chat_container:
        for msg in st.session_state.messages:
            custom_avatar = "🤖" if msg["role"] == "assistant" else "👤"
            st.chat_message(msg["role"], avatar=custom_avatar).write(msg["content"])

    if prompt := st.chat_input("Tanya syarat KK, KTP, atau Akta...", key="chatbot_input_unique"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user", avatar="👤").write(prompt)
            
        with chat_container:
            with st.spinner("Mencari informasi..."):
                if query_engine:
                    try:
                        response = query_engine.query(prompt)
                        reply = str(response)
                    except Exception as e:
                        reply = f"Maaf, terjadi kesalahan teknis: {e}"
                else:
                    reply = "Maaf, basis data atau sistem RAG belum siap."
                
                st.chat_message("assistant", avatar="🤖").write(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})