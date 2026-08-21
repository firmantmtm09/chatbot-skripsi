import os
import streamlit as st
from dotenv import load_dotenv
from frontend.styles import apply_custom_css, render_hero_section

# Import pustaka LlamaIndex & Groq (diambil dari main.py)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.llms.groq import Groq

# Load environment variable
load_dotenv()

st.set_page_config(
    page_title="Portal Resmi Dukcapil DKI Jakarta",
    page_icon="🏛️",
    layout="wide"
)

apply_custom_css()

# ==============================================================================
# FUNGSI INISIALISASI RAG & CHATBOT (Di-cache agar aplikasi tetap ringan & cepat)
# ==============================================================================
@st.cache_resource(show_spinner="Memuat basis pengetahuan Dukcapil...")
def get_query_engine():
    # Mengambil API Key dari file .env (lokal) atau Streamlit Secrets (cloud)
    groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    
    # Inisialisasi Model LLM & Embeddings
    llm = Groq(model="llama3-8b-8192", api_key=groq_api_key, temperature=0, max_tokens=1000)
    
    Settings.llm = llm
    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    Settings.text_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=30)
    
    # Pencarian lokasi folder Data
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(BASE_DIR, "..", "Data"))
    
    if not os.path.exists(data_path):
        data_path = os.path.join(BASE_DIR, "Data")
        
    documents = SimpleDirectoryReader(data_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    
    system_prompt = (
        "Kamu adalah asisten virtual resmi Dukcapil DKI Jakarta. "
        "Jawablah pertanyaan berdasarkan informasi yang ada di dalam context. "
        "Jika informasi tidak ditemukan secara tersurat, cobalah cari makna yang paling mendekati. "
        "Jangan mengurangi atau mengubah angka, syarat, atau ketentuan spesifik yang ada di dalam dokumen. "
        "Gunakan format bullet points dan awali dengan sapaan ramah.\n\n"
        "Context:\n{context_str}\n\n"
        "Pertanyaan: {query_str}\n"
        "Jawaban:"
    )
    
    template = PromptTemplate(system_prompt)
    return index.as_query_engine(text_qa_template=template, similarity_top_k=8)

# Inisialisasi Query Engine
try:
    query_engine = get_query_engine()
except Exception as e:
    query_engine = None
    st.error(f"Gagal memuat basis data chatbot: {e}")

# ==============================================================================
# TAMPILAN PORTAL DUKCAPIL
# ==============================================================================
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
            st.markdown("#### 🎯 Kedudukan, Tugas, dan Fungsi")
            st.write("""
            Berdasarkan Peraturan Gubernur Provinsi Daerah Khusus Ibukota Jakarta Nomor 57 Tahun 2022 tentang Organisasi Dan Tata Kerja Perangkat Daerah mempunyai tugas menyelenggarakan urusan pemerintahan bidang administrasi kependudukan dan pencatatan sipil.

            Untuk melaksanakan tugas sebagaimana dimaksud, Disdukcapil menyelenggarakan fungsi :

            1. penyusunan Rencana Strategis, Rencana Kerja, dan Rencana dan Anggaran Dinas Kependudukan dan Pencatatan Sipil
            2. pelaksanaan Rencana Strategis dan Dokumen Pelaksanaan Anggaran Dinas Kependudukan dan Pencatatan Sipil
            3. perumusan dan pelaksanaan kebijakan, proses bisnis, standar, dan prosedur Dinas Kependudukan dan Pencatatan Sipil
            4. perumusan, pengoordinasian dan pelaksanaan kebijakan urusan pemerintahan di bidang administrasi kependudukan dan pencatatan sipil
            5. pemantauan dan evaluasi pelaksanaan urusan pemerintahan di bidang kependudukan dan pencatatan sipil
            6. pembinaan, pengawasan dan pengendalian urusan pemerintahan di bidang kependudukan dan pencatatan sipil
            7. pelaksanaan kerja sama dan koordinasi dengan PD/UKPD dan/atau instansi pemerintah/swasta/organisasi dalam pelaksanaan urusan pemerintahan di bidang kependudukan dan pencatatan sipil
            8. pengelolaan data dan informasi serta transformasi digital di bidang kependudukan dan pencatatan sipil
            9. pelaksanaan pelayanan pendaftaran penduduk dan pencatatan sipil
            10. pengawasan dan penindakan sesuai dengan ketentuan peraturan perundang-undangan di bidang kependudukan dan pencatatan sipil
            11. penyelesaian permasalahan administrasi kependudukan
            12. pemutakhiran data penduduk dalam pelaksanaan pemilihan umum
            13. pembinaan dan pengembangan peran serta masyarakat dalam administrasi kependudukan
            14. penyusunan profil kependudukan
            15. pembinaan dan pengembangan tenaga fungsional kependudukan dan pencatatan sipil
            16. pelaksanaan kesekretariatan Dinas Kependudukan dan Pencatatan Sipil
            17. pelaksanaan penyediaan dan pengelolaan prasarana dan sarana di bidang kependudukan dan pencatatan sipil
            18. pemberian dukungan teknis kepada masyarakat dan perangkat daerah di bidang administrasi kependudukan dan pencatatan sipil
            19. penegakan peraturan perundang-undangan daerah di bidang administrasi kependudukan dan pencatatan sipil
            20. pelaksanaan koordinasi, pemantauan, evaluasi, pelaporan dan pertanggungjawaban pelaksanaan tugas dan fungsi Dinas Kependudukan dan Pencatatan Sipil dan
            21. pelaksanaan tugas dan fungsi kedinasan lain yang diberikan oleh Gubernur dan/atau Sekretaris Daerah.
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

            st.markdown("<br>", unsafe_allow_html=True)
            st.write("""
            **Denny Wahyu Haryanto** merupakan sosok birokrat berpengalaman yang telah mengabdi dalam pemerintahan selama lebih dari tiga dekade. Beliau memiliki rekam jejak yang luas di berbagai bidang administrasi dan pelayanan publik, khususnya di lingkungan Pemerintah Provinsi DKI Jakarta.
            """)
            
            st.markdown("##### 🎓 Pendidikan Formal")
            st.markdown("""
            * **Diploma III** — Sekolah Tinggi Pemerintahan Dalam Negeri (STPDN), 1993.
            * **Sarjana Ilmu Pemerintahan (S.IP)** — Institut Ilmu Pemerintahan Jakarta, 1998.
            * **Magister Ilmu Pemerintahan (M.Si)** — Universitas Satyagama, 2007.
            """)

            st.markdown("##### 🏅 Pendidikan & Pelatihan Kepemimpinan")
            st.markdown("""
            * Diklat Administrasi Umum (1999)
            * Pendidikan dan Pelatihan Kepemimpinan Tingkat III (2005)
            * Pelatihan Kepemimpinan Nasional Tingkat II (2024)
            """)

            st.markdown("##### 💼 Riwayat Jabatan & Pengalaman Karier")
            st.markdown("""
            * Staf Urusan Pemerintahan di Kecamatan Tanjung Priok, Jakarta Utara (1993)
            * Sekretaris Wilayah Kecamatan Kepulauan Seribu, Jakarta Utara (1999)
            * Wakil Camat Kepulauan Seribu Selatan (2001)
            * Camat Kepulauan Seribu Selatan (2003)
            * Camat Pasar Rebo, Jakarta Timur (2007)
            * Kepala Badan Kesatuan Bangsa Kotamadya Jakarta Timur (2008)
            * Kepala Kantor Kesbangpol Kota Administrasi Jakarta Timur (2009)
            * Kepala Bidang Kewaspadaan, Badan Kesatuan Bangsa dan Politik Provinsi DKI Jakarta (2011)
            * Asisten Pemerintahan Sekretariat Kota Administrasi Jakarta Barat (2012)
            * Kepala Biro Organisasi dan Tatalaksana Setda Provinsi DKI Jakarta (2014)
            * Kepala Badan Penanggulangan Bencana Daerah Provinsi DKI Jakarta (2015)
            * Kepala Biro Administrasi Setda Provinsi DKI Jakarta (2017)
            * Wakil Kepala Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu Provinsi DKI Jakarta (2017)
            * **Kepala Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta (2025 – Sekarang)**
            """)

            st.write("""
            Dengan pengalaman yang komprehensif di bidang pemerintahan, administrasi, dan pelayanan publik, beliau berkomitmen penuh untuk mewujudkan pelayanan administrasi kependudukan yang profesional, transparan, dan akuntabel bagi seluruh warga Jakarta.
            """)
        elif sub_menu_profil == "Profil Pejabat":
            st.markdown("#### 👥 Profil Pejabat Struktural")
            st.write("Daftar Pemangku Jabatan Struktural di Lingkungan Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta:")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            pejabat_list = [
                {"jabatan": "Kepala Dinas Kependudukan dan Pencatatan Sipil", "nama": "Drs. Denny Wahyu Haryanto, M.Si"},
                {"jabatan": "Sekretaris Dinas Kependudukan dan Pencatatan Sipil", "nama": "Muhammad Nurrahman, S.Kom, MM"},
                {"jabatan": "Kepala Bidang Pendaftaran Penduduk", "nama": "Shanti, S.Sos, MA"},
                {"jabatan": "Kepala Bidang Pencatatan Sipil", "nama": "Witri Yenny, S.Sos, M.Si"},
                {"jabatan": "Kepala Bidang Data dan Informasi", "nama": "Firman, ST"},
                {"jabatan": "Kepala Bidang Pembinaan, Pengawasan dan Pengendalian Adminduk", "nama": "Sudirman, SH"},
                {"jabatan": "Kepala Unit", "nama": "Desmond, S.Si, MM"},
                {"jabatan": "Kepala Unit Pengelola Teknologi Informasi Kependudukan", "nama": "Hari Wibowo, MAP"}
            ]
            
            for p in pejabat_list:
                st.markdown(f"""
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px 18px; border-radius: 12px; margin-bottom: 10px;">
                    <div style="font-size: 13px; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;">{p['jabatan']}</div>
                    <div style="font-size: 16px; font-weight: 700; color: #1E293B; margin-top: 4px;">{p['nama']}</div>
                </div>
                """, unsafe_allow_html=True)
        elif sub_menu_profil == "Sejarah":
            st.markdown("#### 📜 Sejarah Singkat Dinas Dukcapil")
            
            st.markdown("##### **Latar Belakang Dinas Dukcapil**")
            st.write("""
            Pada awal abad XIX, kota Batavia (Jakarta) mengalami perkembangan dan perubahan yang pesat terutama di bidang pemerintahan. Batavia merupakan kota yang menjadi pusat pemerintahan dan perdagangan pada masa kolonial Belanda. Dengan dibangunnya infrastruktur seperti pusat ibadah, gedung kesenian, kantor pos, gedung mahkamah agung, Lapangan Banteng, hingga Lapangan Monas, mengindikasikan Batavia akan menjadi ibu kota. 
            
            Seiring dengan pembangunannya, kebutuhan penyelenggaraan tertib administrasi kependudukan dan pencatatan sipil (*Burgerlijk Stand*) sudah mulai terorganisir, dibuktikan dengan dokumen akta pencatatan sipil bertahun 1829. Penyelenggaraannya mengacu pada peraturan perundang-undangan Belanda (asas konkordansi) yang hanya berlaku bagi warga Belanda, Eropa, dan Amerika.
            """)

            st.markdown("##### **Perkembangan Ordonansi Pencatatan Sipil**")
            st.write("""
            Ordonansi pencatatan sipil yang pertama dibuat untuk daerah Hindia Belanda diberlakukan pada tahun 1850 dengan ditetapkannya Ordonantie Catatan Sipil bagi Golongan Eropa di Hindia Belanda, yaitu *Reglement* tentang daftar-daftar pencatatan sipil bagi bangsa Eropa, Indonesia Asli (Bumi Putera), dan mereka yang dipersamakan dengan bangsa Eropa (yaitu mereka yang menundukkan diri secara sukarela kepada hukum sipil/perdata dan hukum dagang Eropa, Staatsblad Tahun 1849 Nomor 25).
            
            Terbatasnya pelayanan catatan sipil tersebut sejalan dengan politik Pemerintah Hindia Belanda yang membagi dan menggolongkan penduduk berdasarkan Pasal 131 dan 163 IS (*Indische Staatsregeling*) menjadi 3 golongan: Golongan Eropa, Timur Asing, dan Pribumi.
            """)

            st.markdown("##### **Masa Pendudukan Jepang (1942–1945)**")
            st.write("""
            Pada masa pendudukan Jepang, nama *Bergerlijke Stand* (BS) diganti menjadi **"Cacah Jiwa"** dan lembaganya disebut **"Kantor Pencacah Jiwa"**. Penggunaan istilah "jiwa" diambil dari bunyi Kitab Undang-Undang Hukum Sipil bahwa catatan sipil diartikan sebagai "pendaftaran jiwa". Nomor dan penanggalan akta pada masa ini menggunakan tahun penanggalan Jepang.
            """)

            st.markdown("##### **Pasca Kemerdekaan dan Era Orde Baru**")
            st.write("""
            Setelah Proklamasi Kemerdekaan 17 Agustus 1945, penyelenggaraan pencatatan sipil diambil alih oleh Pemerintah Republik Indonesia. Berdasarkan hasil Kongres Bahasa ke-2 di Medan pada tahun 1950, istilah *Bergerlijke Stand* diterjemahkan secara resmi menjadi **Catatan Sipil**.
            
            Pada masa pemerintahan Walikota Soediro menjelang tahun 1957, Jakarta berubah status menjadi Daerah Istimewa (Chusus) Tingkat I. Kantor catatan sipil di Jakarta kemudian disatukan menjadi **Kantor Catatan Sipil DCI Jakarta Raya** yang berlokasi di Jl. Pintu Besar Utara No. 12 Kota, dengan Kepala Kantor pertama yang dijabat oleh orang Indonesia setelah kemerdekaan yaitu **Bapak H. Pratiknyo**.
            
            Perubahan politik mendasar terjadi pasca peristiwa G30S/PKI pada tahun 1965 di bawah Pemerintahan Orde Baru pimpinan Presiden Soeharto. Melalui Instruksi Presidium Kabinet Ampera No. 31/In/U/12/66, penyelenggaraan catatan sipil dinyatakan terbuka untuk seluruh penduduk, baik Warga Negara Indonesia maupun Warga Negara Asing, yang menjadi landasan kuat bagi arah kebijakan dan perkembangan pembangunan layanan kependudukan di Indonesia hingga saat ini.
            """)

    with selected_tab[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌐 Sistem Layanan Online Masyarakat")
        st.write("Silakan pilih ekosistem aplikasi resmi Disdukcapil DKI Jakarta sesuai dengan kebutuhan administrasi Anda:")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_layanan_1, col_layanan_2 = st.columns(2, gap="medium")
        
        with col_layanan_1:
            st.markdown("""
            <div style="background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 16px; padding: 24px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="color: #92400E; margin-top: 0; font-weight: 700;">🥑 Alpukat Betawi</h4>
                    <p style="color: #78350F; font-size: 13px; font-weight: 600; margin-bottom: 8px;">Akses Langsung Pelayanan Dokumen Cepat & Akurat</p>
                    <p style="color: #92400E; font-size: 13px; line-height: 1.5;">Platform mandiri terintegrasi untuk pengajuan Akta Kelahiran, Pencatatan Kartu Keluarga (KK), Kartu Identitas Anak (KIA), surat keterangan Pindah Datang, serta sinkronisasi database kependudukan secara real-time.</p>
                </div>
                <div style="margin-top: 20px;">
                    <a href="https://alpukat-dukcapil.jakarta.go.id/" target="_blank" style="background: #D97706; color: white; padding: 10px 18px; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 13px; display: inline-block;">Buka Alpukat Betawi →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_layanan_2:
            st.markdown("""
            <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 16px; padding: 24px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="color: #166534; margin-top: 0; font-weight: 700;">📱 Identitas Kependudukan Digital (IKD)</h4>
                    <p style="color: #14532D; font-size: 13px; font-weight: 600; margin-bottom: 8px;">KTP Digital dalam Genggaman Anda</p>
                    <p style="color: #166534; font-size: 13px; line-height: 1.5;">Aplikasi resmi dari Ditjen Dukcapil Kemendagri untuk mentransformasikan KTP fisik ke dalam smartphone Anda. Dilengkapi dengan fitur QR Code aman untuk proses verifikasi data tanpa perlu berkas fotokopi.</p>
                </div>
                <div style="margin-top: 20px;">
                    <a href="https://www.instagram.com/p/CpKUXYhpUwx/" target="_blank" style="background: #16A34A; color: white; padding: 10px 18px; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 13px; display: inline-block;">Panduan Aktivasi IKD →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #FFFBEB; border-left: 5px solid #F59E0B; padding: 14px 18px; border-radius: 10px;">
            <span style="font-weight: 700; color: #92400E; font-size: 13px;">⚠️ Catatan Penting:</span>
            <span style="color: #92400E; font-size: 13px;"> Pastikan Anda menggunakan data perseorangan yang valid saat registrasi untuk menghindari penolakan sistem otomatis.</span>
        </div>
        """, unsafe_allow_html=True)

    with selected_tab[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚖️ Dasar Hukum & Regulasi Adminduk")
        st.write("Klik pada judul regulasi di bawah ini untuk melihat detail peraturan:")
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("📄 UU Nomor 24 Tahun 2013 tentang Administrasi Kependudukan"):
            st.write("Perubahan atas Undang-Undang Nomor 23 Tahun 2006 yang menegaskan bahwa pengurusan dan penerbitan dokumen kependudukan **tidak dipungut biaya (GRATIS)** bagi seluruh warga negara.")
        
        with st.expander("📄 Perpres Nomor 96 Tahun 2018"):
            st.write("Mengatur tentang Tata Cara Pendaftaran Penduduk dan Pencatatan Sipil, yang memangkas berbagai birokrasi dan syarat pengantar (RT/RW) untuk beberapa jenis dokumen transisi.")
            
        with st.expander("📄 Pergub DKI Jakarta Nomor 57 Tahun 2022"):
            st.write("Peraturan Gubernur mengenai Organisasi dan Tata Kerja Perangkat Daerah, yang mendasari fungsi, kedudukan, serta wewenang operasional Disdukcapil Provinsi DKI Jakarta.")

    with selected_tab[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📞 Hubungi Kami")
        st.write("Hubungi pusat bantuan atau kunjungi kantor operasional kami melalui detail informasi di bawah ini:")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2, gap="medium")
        
        with col_c1:
            st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #1E293B; font-size: 15px; margin-bottom: 8px;">📍 Alamat Kantor Pusat</div>
                <div style="font-weight: 600; color: #334155; font-size: 13px; margin-bottom: 4px;">Dinas Kependudukan dan Pencatatan Sipil DKI Jakarta</div>
                <div style="color: #64748B; font-size: 13px; line-height: 1.5;">Jl. Letjen S. Parman No.7, RT.3/RW.3, Tomang, Kec. Grogol petamburan, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11440</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px;">
                <div style="font-weight: 700; color: #1E293B; font-size: 15px; margin-bottom: 8px;">✉️ Korespondensi Email</div>
                <div style="color: #64748B; font-size: 13px; margin-bottom: 6px;">Kirimkan surat elektronik resmi instansi atau pertanyaan umum ke:</div>
                <div style="font-weight: 600; color: #2563EB; font-size: 13px;">dinas_dukcapil@jakarta.go.id</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_c2:
            st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px; margin-bottom: 16px;">
                <div style="font-weight: 700; color: #1E293B; font-size: 15px; margin-bottom: 8px;">💬 WhatsApp Pengaduan & Hotline</div>
                <div style="color: #64748B; font-size: 13px; margin-bottom: 6px;">Masyarakat dapat melakukan konsultasi aktif pada hari kerja:</div>
                <div style="font-weight: 700; color: #16A34A; font-size: 15px; margin-bottom: 4px;">+81212012031</div>
                <div style="color: #64748B; font-size: 12px;">🕒 Senin - Jumat | 08.00 - 16.00 WIB</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px;">
                <div style="font-weight: 700; color: #1E293B; font-size: 15px; margin-bottom: 8px;">🌐 Media Sosial Resmi</div>
                <div style="color: #64748B; font-size: 13px; margin-bottom: 6px;">Pantau informasi infografis terkini melalui kanal berita digital kami:</div>
                <div style="color: #334155; font-size: 13px; line-height: 1.6;">
                    📸 Instagram: <b>@dukcapiljakarta</b><br>
                    🐦 X / Twitter: <b>@dukcapiljakarta</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #EFF6FF; border-left: 5px solid #3B82F6; padding: 14px 18px; border-radius: 10px;">
            <span style="font-weight: 700; color: #1E40AF; font-size: 13px;">🚇 Akses Transportasi:</span>
            <span style="color: #1E40AF; font-size: 13px;"> Kantor pusat berlokasi strategis di koridor utama koridor S. Parman, sangat dekat dari halte integrasi TransJakarta Tomang.</span>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# LOGIKA FITUR CHATBOT DI KOLOM KANAN
# ==============================================================================
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
                if query_engine is not None:
                    try:
                        # Eksekusi RAG LlamaIndex secara langsung tanpa HTTP Request
                        response = query_engine.query(prompt)
                        reply = str(response)
                    except Exception as e:
                        reply = f"Maaf, terjadi kesalahan teknis saat memproses jawaban: {e}"
                else:
                    reply = "Maaf, sistem RAG belum siap atau dokumen belum berhasil dimuat."
                
                st.chat_message("assistant", avatar="🤖").write(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})