import streamlit as st
from frontend.styles import apply_custom_css, render_hero_section
import os
import requests

st.set_page_config(
    page_title="Portal Resmi Dukcapil DKI Jakarta",
    page_icon="🏛️",
    layout="wide"
)

apply_custom_css()

BACKEND_API_URL = "https://unbounded-shush-widen.ngrok-free.dev/chat"

st.markdown("""
<style>
    /* Mengurangi padding bawaan wide layout biar muat sempurna */
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
            
            st.markdown("##### **Untuk melaksanakan tugas sebagaimana dimaksud, Disdukcapil menyelenggarakan fungsi :**")
            st.write("""
            * Penyusunan Rencana Strategis, Rencana Kerja, dan Rencana dan Anggaran Dinas Kependudukan dan Pencatatan Sipil;
            * Pelaksanaan Rencana Strategis dan Dokumen Pelaksanaan Anggaran Dinas Kependudukan dan Pencatatan Sipil;
            * Perumusan dan pelaksanaan kebijakan, proses bisnis, standar, dan prosedur Dinas Kependudukan dan Pencatatan Sipil;
            * Perumusan, pengoordinasian dan pelaksanaan kebijakan urusan pemerintahan di bidang administrasi kependudukan dan pencatatan sipil;
            * Pemantauan dan evaluasi pelaksanaan urusan pemerintahan di bidang kependudukan dan pencatatan sipil;
            * Pembinaan, pengawasan dan pengendalian urusan pemerintahan di bidang kependudukan dan pencatatan sipil;
            * Pelaksanaan kerja sama dan koordinasi dengan PD/UKPD dan/atau instansi pemerintah/swasta/organisasi dalam pelaksanaan urusan pemerintahan di bidang kependudukan dan pencatatan sipil;
            * Pengelolaan data dan informasi serta transformasi digital di bidang kependudukan dan pencatatan sipil;
            * Pelaksanaan pelayanan pendaftaran penduduk dan pencatatan sipil;
            * Pengawasan dan penindakan sesuai dengan ketentuan peraturan perundang-undangan di bidang kependudukan dan pencatatan sipil;
            * Penyelesaian permasalahan administrasi kependudukan;
            * Pemutakhiran data penduduk dalam pelaksanaan pemilihan umum;
            * Pembinaan dan pengembangan peran serta masyarakat dalam administrasi kependudukan;
            * Penyusunan profil kependudukan;
            * Pembinaan dan pengembangan tenaga fungsional kependudukan dan pencatatan sipil;
            * Pelaksanaan kesekretariatan Dinas Kependudukan dan Pencatatan Sipil;
            * Pelaksanaan penyediaan dan pengelolaan prasarana dan sarana di bidang kependudukan dan pencatatan sipil;
            * Pemberian dukungan teknis kepada masyarakat dan perangkat daerah di bidang administrasi kependudukan dan pencatatan sipil;
            * Penegakan peraturan perundang-undangan daerah di bidang administrasi kependudukan dan pencatatan sipil;
            * Pelaksanaan koordinasi, pemantauan, evaluasi, pelaporan dan pertanggungjawaban pelaksanaan tugas dan fungsi Dinas Kependudukan dan Pencatatan Sipil; dan
            * Pelaksanaan tugas dan fungsi kedinasan lain yang diberikan oleh Gubernur dan/atau Sekretaris Daerah.
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
                st.write("""
                Denny Wahyu Haryanto merupakan sosok birokrat berpengalaman yang telah mengabdi dalam pemerintahan selama lebih dari tiga dekade. Beliau memiliki rekam jejak yang luas di berbagai bidang administrasi dan pelayanan publik, khususnya di lingkungan Pemerintah Provinsi DKI Jakarta.
                """)
                
                st.markdown("🔗 **Pendidikan Formal:**")
                st.write("""
                * **Diploma III** – Sekolah Tinggi Pemerintahan Dalam Negeri (STPDN) (1993)
                * **Sarjana Ilmu Pemerintahan** – Institut Ilmu Pemerintahan Jakarta (1998)
                * **Magister Ilmu Pemerintahan** – Universitas Satyagama (2007)
                """)
                
                st.markdown("📚 **Pengembangan Kompetensi & Diklat Strategis:**")
                st.write("""
                * Diklat Administrasi Umum (1999)
                * Pendidikan dan Pelatihan Kepemimpinan Tingkat III (2005)
                * Pelatihan Kepemimpinan Nasional Tingkat II (2024)
                """)
                
                st.markdown("💼 **Perjalanan Karier & Posisi Strategis:**")
                st.write("""
                Kariernya di lingkungan pemerintahan dimulai sebagai Staf Urusan Pemerintahan di Kecamatan Tanjung Priok, Jakarta Utara pada tahun 1993, hingga dipercaya menduduki berbagai posisi berikut:
                * **1999:** Sekretaris Wilayah Kecamatan Kepulauan Seribu, Jakarta Utara
                * **2001:** Wakil Camat Kepulauan Seribu Selatan
                * **2003:** Camat Kepulauan Seribu Selatan
                * **2007:** Camat Pasar Rebo, Jakarta Timur
                * **2008:** Kepala Badan Kesatuan Bangsa Kotamadya Jakarta Timur
                * **2009:** Kepala Kantor Kesbangpol Kota Administrasi Jakarta Timur
                * **2011:** Kepala Bidang Kewaspadaan, Badan Kesatuan Bangsa dan Politik Provinsi DKI Jakarta
                * **2012:** Asisten Pemerintahan Sekretariat Kota Administrasi Jakarta Barat
                * **2014:** Kepala Biro Organisasi dan Tatalaksana Setda Provinsi DKI Jakarta
                * **2015:** Kepala Badan Penanggulangan Bencana Daerah Provinsi DKI Jakarta
                * **2017:** Kepala Biro Administrasi Setda Provinsi DKI Jakarta
                * **2017:** Wakil Kepala Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu Provinsi DKI Jakarta
                """)
                
                st.write("""
                Dengan pengalaman yang komprehensif di bidang pemerintahan, administrasi, dan pelayanan publik, pada tahun **2025** beliau dipercaya untuk mengemban amanah sebagai **Kepala Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta**. Dalam posisi ini, beliau berkomitmen untuk mewujudkan pelayanan administrasi kependudukan yang profesional, transparan, and akuntabel bagi seluruh warga Jakarta.
                """)

        elif sub_menu_profil == "Profil Pejabat":
            st.markdown("#### 👥 Profil Pejabat Struktural")
            st.write("""
            Daftar Pemangku Jabatan Struktural Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta:
            - **Kepala Dinas:** Denny Wahyu Haryanto
            - **Wakil Kepala Dinas:** (Dalam Masa Transisi / Pembaruan)
            - **Sekretaris Dinas:** Yadi Rusmayadi, S.E., M.Si.
            - **Kepala Bidang Pelayanan Pendaftaran Penduduk:** Dra. Diana Indriati
            - **Kepala Bidang Pelayanan Pencatatan Sipil:** Haris Tokoh, S.H., M.H.
            - **Kepala Bidang Data dan Informasi:** Muhammad Nur, S.Kom., M.T.
            """)

        elif sub_menu_profil == "Sejarah":
            st.markdown("#### 📜 Sejarah Singkat")
            
            st.markdown("### **LATAR BELAKANG DINAS DUKCAPIL**")
            st.write("""
            Pada awal abad XIX, kota Batavia (Jakarta) mengalami perkembangan dan perubahan yang pesat terutama di bidang Pemerintahan. 
            Batavia merupakan Kota yang menjadi pusat Pemerintahan dan perdagangan pada saat kolonial Belanda. Dengan dibangunnya infrastruktur 
            sperti pusat Ibadah, Gd. Kesenian, Kantor Pos, Gd. Mahkamah Agung, lapangan Banteng, hingga lapangan Monas sehingga mengindikasikan 
            Batavia akan menjadi Ibukota. 
            
            Seiring dengan pembangunannya maka kebutuhan penyelenggaraan tertib administrasi kependudukan dan pencatatan sipil (*Burgerlijk Stand*) 
            sudah mulai terorganisir dibuktikan dengan dokumen akta pencatatan sipil bertahun 1829. Penyelenggaraannya mengacu pada peraturan 
            perundang-undangan Belanda (asas konkordansi) hanya berlaku bagi warga Belanda, Eropa dan Amerika.
            """)
            
            st.markdown("---")
            st.markdown("🏛️ **Era Ordonansi Catatan Sipil (1850)**")
            st.write("""
            Ordonansi pencatatan sipil yang pertama dibuat untuk daerah Hindia Belanda, diberlakukan pada tahun 1850, dengan ditetapkannya *ordonantie* Catatan Sipil bagi Golongan Eropa di Hindia Belanda, yaitu Reglement tentang hal daftar-daftar pencatatan sipil bagi Bangsa Eropa dan juga 
            Indonesia Asli (Bumi Putera) dan mereka yang dipersamakan dengan bangsa itu (Eropa) yaitu mereka yang menundukkan diri menurut ketentuan 
            perundang-undangan kepada seluruhnya dengan sukarela kepada hukum sipil (perdata) dan hukum dagang yang diterapkan bagi Bangsa Eropa 
            *(Staatsblad Tahun 1849 Nomor 25)*.
            
            Terbatasnya pelayanan Catatan Sipil tersebut adalah sejalan dengan politik Pemerintah Hindia Belanda yang membagi dan menggolongkan 
            penduduk dan kemudian bagi setiap golongan penduduk berlaku hukum yang berbeda. Didasari ketentuan Pasal 131 dan 163 IS *(Indische Staatsregeling)* ada 3 golongan penduduk yaitu Golongan Eropa, Timur Asing dan Pribumi.
            """)
            
            st.markdown("---")
            st.markdown("⚔️ **Masa Pendudukan Jepang (1942 - 1945)**")
            st.write("""
            Pada masa pendudukan Jepang tersebut tidak banyak terdapat keterangan tentang penyelenggaraan pencatatan sipil, kecuali dalam daftar register 
            akta catatan sipil pada masa itu (1942-1945) diketahui bahwa nama *Burgerlijke Stand* (BS) diganti menjadi **“Cacah Jiwa”** dan lembaganya 
            disebut **“Kantor Pencacah Jiwa”**. 
            
            Penggunaan Istilah “jiwa” diambil dari bunyi Kitab Undang Undang Hukum Sipil, yaitu bahwa kata Catatan Sipil diartikan sebagai “pendaftaran jiwa”. 
            Adapun nomor dan penanggalan akta Kantor Pencacah Jiwa tersebut menggunakan tahun penanggalan Jepang.
            """)
            
            st.markdown("---")
            st.markdown("🇮🇩 **Era Kemerdekaan & Peralihan (1945 - 1957)**")
            st.write("""
            Setelah kemederkaan RI pada tanggal 17 Agustus 1945, penyelenggaraan Pencatatan Sipil diambil alih oleh Pemerintah Republik Indonesia dan 
            Lembaga *Burgerlijke Stand* (BS)/Kantor Pencacah Jiwa dilanjutkan kegiatannya dengan meneruskan apa-apa yang dahulu dikerjakan oleh lembaga ini, 
            termasuk namanya masih menggunakan *Burgerlijke Stand* (BS).
            
            Belum dapat diketahui secara pasti kapan BS itu secara resmi diganti menjadi Kantor Catatan Sipil, informasi yang diperoleh dari Ibu Khatidjah Wasito 
            (Kepala Seksi Penyuluhan dan Evaluasi Kantor Catatan Sipil Pemerintah DKI Jakarta 1984-1989), menyebutkan BS diterjemahkan menjadi Catatan Sipil 
            pada Kongres Bahasa ke-2 di Medan pada Tahun 1950. Istilah itu diambil atas dasar adanya istilah Pegawai Luar Biasa Pencatat Sipil dalam KUH Perdata.
            
            Pada tanggal 17 Agustus 1945 sehari setelahnya lahir Undang-undang Dasar 1945, secara resmi berdiri pemerintahan peralihan Ibukota Republik Indonesia Jakarta, 
            dengan Soewirjo sebagai Walikota pertamanya. Pada masa itu di Jakarta terdapat 2 Kantor Catatan Sipil, yaitu Kantor Catatan Sipil Batavia berlokasi di 
            Jl. Perwira (sekarang Mesjid Istiqlal) dan satunya lagi Kantor Catatan Sipil Mister Cornelis (Jatinegara, sekarang berlokasi di depan Stasiun Kereta Api Jatinegara).
            """)
            
            st.markdown("---")
            st.markdown("🌆 **Penyatuan Kantor Catatan Sipil DKI**")
            st.write("""
            Pada masa pemerintahan Walikota Soediro menjelang tahun 1957, kota Jakarta berubah status menjadi Daerah Istimewa (Chusus) Tingkat I dan dipimpin oleh seorang Gubernur. 
            Pada periode ini pulalah lembaga *burgerlijke stand* diganti namanya menjadi Kantor Catatan Sipil, sebagai salah satu hasil dari Kongres Bahasa ke-2 di Medan. 
            
            Adapun Tentang Pegawai Luar Biasa Pencatat Sipil atau penandatangan akta catatan Sipil di Jakarta, sejak tahun 1829 sampai dengan 1942 and 1945 sampai akhir revolusi 
            fisik tahun 1949 penyerahan kedaulatan oleh sekutu (Belanda) kepada pemerintah Indonesia, BS masih dijabat oleh orang Belanda. Diantaranya adalah: *de hoost Simon Petrus Marinas*, 
            *Johannes Leonard Domingos* dan seorang Indonesia bernama: **Ahmad Badaruddin**. 
            
            Berkenaan dengan perluasan Daerah Khusus Ibukota Jakarta inilah, kemudian Kantor Catatan Sipil di Jakarta menjadi satu, yaitu **Kantor Catatan Sipil DCI Jakarta Raya** yang berlokasi di Jl. Pintu Besar Utara No. 12 Kota (di belakang Gedung Museum Wayang sekarang). Sedangkan Kantor Catatan Sipil Mister Cornelis dihapuskan dan sebagian 
            dari Akta-akta Catatan Sipil yang ada diserahkan ke Kantor Catatan Sipil DCI Djakarta dan sebagian lainnya diserahkan ke Kantor Catatan Sipil Kabupaten Bekasi. Kepala Kantor 
            Catatan Sipil DCI Jakarta pertama yang dijabat oleh Orang Indonesia setelah Kemerdekaan adalah **Bapak H. Pratiknyo**.
            """)
            
            st.markdown("---")
            st.markdown("📈 **Era Orde Baru & Keterbukaan Pelayanan**")
            st.write("""
            Terjadinya perubahan politik yang mendasar di Indonesia, sebagai akibat dari peristiwa pemberontakan G 30 S PKI pada tahun 1965 yang berhasil ditumbangkan oleh 
            Pemerintah Republik Indonesia, maka Negara Indonesia memulai Pemerintahan Orde Baru dengan kepemimpinan Bapak Soeharto sebagai Presiden RI. 
            
            Pemerintahan Orde Baru tersebut membuka era baru pula dalam penyelenggaraan Catatan Sipil di Indonesia, yaitu melalui **Instruksi Presidium Kabinet Ampera No.31/In/U/12/66** penyelenggaraan Catatan Sipil dinyatakan terbuka untuk seluruh penduduk Warga Negara Indonesia maupun Warga Negara Asing. 
            Instruksi tersebut memberi landasan hukum sebagai jawaban kebutuhan pelayanan catatan sipil oleh masyarakat dan membawa pengaruh yang besar bagi arah kebijakan 
            dan perkembangan pembangunan di bidang Catatan Sipil selanjutnya di Indonesia.
            """)

    with selected_tab[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌐 Sistem Layanan Online Masyarakat")
        st.write("Silakan pilih ekosistem aplikasi resmi Disdukcapil DKI Jakarta sesuai dengan kebutuhan administrasi Anda:")
        
        st.markdown("""
        <style>
            .online-service-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin-top: 15px;
                margin-bottom: 25px;
            }
            .service-card {
                border-radius: 16px;
                padding: 24px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                min-height: 220px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .service-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.06);
            }
            .bg-alpukat-box {
                background-color: #FFFBEB;
                border: 1px solid #FDE68A;
            }
            .bg-ikd-box {
                background-color: #F0FDF4;
                border: 1px solid #BBF7D0;
            }
            .service-header {
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .color-alpukat-text { color: #92400E; }
            .color-ikd-text { color: #166534; }
            
            .service-body {
                font-size: 13.5px;
                color: #4B5563;
                line-height: 1.6;
                margin-bottom: 20px;
            }
            .btn-service {
                display: inline-block;
                text-align: center;
                padding: 10px 16px;
                border-radius: 10px;
                font-size: 13.0px;
                font-weight: 600;
                text-decoration: none !important;
                transition: background 0.2s ease;
                width: fit-content;
            }
            .btn-alpukat {
                background-color: #D97706;
                color: white !important;
            }
            .btn-alpukat:hover { background-color: #B45309; }
            
            .btn-ikd {
                background-color: #16A34A;
                color: white !important;
            }
            .btn-ikd:hover { background-color: #15803D; }
        </style>
        """, unsafe_allow_html=True)
        
        html_code = (
            "<div class='online-service-grid'>"
            "    <div class='service-card bg-alpukat-box'>"
            "        <div>"
            "            <div class='service-header color-alpukat-text'>🥑 Alpukat Betawi</div>"
            "            <div class='service-body'>"
            "                <b>Akses Langsung Pelayanan Dokumen Cepat & Akurat</b><br>"
            "                Platform mandiri terintegrasi untuk pengajuan Akta Kelahiran, Pencetakan Kartu Keluarga (KK), Kartu Identitas Anak (KIA), surat keterangan Pindah Datang, serta sinkronisasi database kependudukan secara real-time."
            "            </div>"
            "        </div>"
            "        <a class='btn-service btn-alpukat' href='https://alpukat-dukcapil.jakarta.go.id/' target='_blank'>Buka Alpukat Betawi →</a>"
            "    </div>"
            "    <div class='service-card bg-ikd-box'>"
            "        <div>"
            "            <div class='service-header color-ikd-text'>📱 Identitas Kependudukan Digital (IKD)</div>"
            "            <div class='service-body'>"
            "                <b>KTP Digital dalam Genggaman Anda</b><br>"
            "                Aplikasi resmi dari Ditjen Dukcapil Kemendagri untuk mentransformasikan KTP fisik ke dalam smartphone Anda. Dilengkapi dengan fitur QR Code aman untuk proses verifikasi data tanpa perlu berkas fotokopi."
            "            </div>"
            "        </div>"
            "        <a class='btn-service btn-ikd' href='https://www.instagram.com/p/CpKUXYhpUwx/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==' target='_blank'>Panduan Aktivasi IKD →</a>"
            "    </div>"
            "</div>"
        )
        st.markdown(html_code, unsafe_allow_html=True)
        
        st.warning("⚠️ **Catatan Penting:** Pastikan Anda menggunakan data perseorangan yang valid saat registrasi untuk menghindari penolakan sistem otomatis.")

    with selected_tab[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚖️ Dasar Hukum & Regulasi Adminduk")
        st.write("Klik pada judul regulasi di bawah ini untuk melihat detail peraturan:")
        
        with st.expander("📄 UU Nomor 24 Tahun 2013 tentang Administrasi Kependudukan"):
            st.write("""
            Perubahan atas Undang-Undang Nomor 23 Tahun 2006 yang menegaskan bahwa pengurusan dan penerbitan dokumen kependudukan 
            **tidak dipungut biaya (GRATIS)** bagi seluruh warga negara.
            """)
            
        with st.expander("📄 Perpres Nomor 96 Tahun 2018"):
            st.write("""
            Mengatur tentang Tata Cara Pendaftaran Penduduk dan Pencatatan Sipil, yang memangkas berbagai birokrasi dan syarat pengantar (RT/RW) untuk beberapa jenis dokumen transisi.
            """)
            
        with st.expander("📄 Pergub DKI Jakarta Nomor 57 Tahun 2022"):
            st.write("""
            Peraturan Gubernur mengenai Organisasi dan Tata Kerja Perangkat Daerah, yang mendasari fungsi, kedudukan, serta wewenang operasional Disdukcapil Provinsi DKI Jakarta.
            """)

    with selected_tab[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📞 Hubungi Kami")
        st.write("Hubungi pusat bantuan atau kunjungi kantor operasional kami melalui detail informasi di bawah ini:")
        
        st.markdown("""
        <style>
            .contact-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px;
                margin-top: 15px;
                margin-bottom: 25px;
            }
            .contact-card {
                background-color: #FAFAFA;
                border: 1px solid #E5E5E5;
                border-radius: 14px;
                padding: 20px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .contact-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.04);
            }
            .contact-title {
                font-size: 15px;
                font-weight: 700;
                color: #1F2937;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .contact-text {
                font-size: 13px;
                color: #4B5563;
                line-height: 1.5;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-grid">
            <!-- Kotak 1: Alamat -->
            <div class="contact-card">
                <div class="contact-title">📍 Alamat Kantor Pusat</div>
                <div class="contact-text">
                    <b>Dinas Kependudukan dan Pencatatan Sipil DKI Jakarta</b><br>
                    Jl. Letjen S. Parman No.7, RT.3/RW.3, Tomang, Kec. Grogol Petamburan, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta 11440
                </div>
            </div>
            <!-- Kotak 2: Pengaduan/Hotline -->
            <div class="contact-card">
                <div class="contact-title">💬 WhatsApp Pengaduan & Hotline</div>
                <div class="contact-text">
                    Masyarakat dapat melakukan konsultasi aktif pada hari kerja:<br>
                    <b>+62 811-1234-5678</b><br>
                    <span style="font-size: 11px; color: #9CA3AF;">⏰ Senin - Jumat | 08.00 - 16.00 WIB</span>
                </div>
            </div>
            <!-- Kotak 3: Email -->
            <div class="contact-card">
                <div class="contact-title">📧 Korespondensi Email</div>
                <div class="contact-text">
                    Kirimkan surat elektronik resmi instansi atau pertanyaan umum ke:<br>
                    <a href="mailto:dinas_dukcapil@jakarta.go.id" style="color: #2563EB; font-weight: 600; text-decoration: none;">dinas_dukcapil@jakarta.go.id</a>
                </div>
            </div>
            <!-- Kotak 4: Media Sosial -->
            <div class="contact-card">
                <div class="contact-title">🌐 Media Sosial Resmi</div>
                <div class="contact-text">
                    Pantau informasi infografis terkini melalui kanal berita digital kami:<br>
                    📸 Instagram: <a href="https://www.instagram.com/dukcapiljakarta/" target="_blank" style="color: #2563EB; text-decoration:none;">@dukcapiljakarta</a><br>
                    🐦 X / Twitter: <a href="https://x.com/dukcapiljakarta target="_blank" style="color: #2563EB; text-decoration:none;">@dukcapiljakarta</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🗺️ **Akses Transportasi:** Kantor pusat berlokasi strategis di koridor utama koridor S. Parman, sangat dekat dari halte integrasi TransJakarta Tomang.")

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
                try:
                    response = requests.post(BACKEND_API_URL, json={"message": prompt}, timeout=30)
                    if response.status_code == 200:
                        reply = response.json().get("reply", "Maaf, sistem tidak memberikan respon valid.")
                    else:
                        reply = "Gagal terhubung ke API Backend."
                except Exception as e:
                    reply = f"Gagal menghubungi server AI. (Error: {e})"
                
                st.chat_message("assistant", avatar="🤖").write(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        