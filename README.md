# 🏛️ Chatbot Layanan Publik Dukcapil DKI Jakarta
> Asisten Virtual berbasis RAG (Retrieval-Augmented Generation) untuk layanan informasi administrasi kependudukan Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta.

---

## 📌 Tentang Proyek

Proyek ini merupakan implementasi chatbot layanan publik yang dikembangkan sebagai bagian dari penelitian skripsi. Sistem ini memungkinkan masyarakat untuk mendapatkan informasi seputar persyaratan dan prosedur pengurusan dokumen kependudukan seperti KK, KTP-el, dan Akta Catatan Sipil secara cepat dan akurat tanpa harus datang langsung ke kantor.

Chatbot ini menggunakan metode **Retrieval-Augmented Generation (RAG)** — pendekatan yang menggabungkan kemampuan pencarian dokumen dengan model bahasa besar, sehingga jawaban yang diberikan selalu berbasis dokumen resmi dan dapat dipertanggungjawabkan.

---

## 🧱 Arsitektur Sistem

```
User Input
    │
    ▼
Streamlit UI (app.py)
    │
    ▼
LlamaIndex RAG Pipeline
    ├── Embedding  : BAAI/bge-small-en-v1.5 (HuggingFace)
    ├── Vector Store: VectorStoreIndex (In-Memory)
    └── LLM        : openai/gpt-oss-20b via Groq API
    │
    ▼
Knowledge Base (Data/Dokumen_LayananPublik.pdf)
    │
    ▼
Response → User
```

---

## 🗂️ Struktur Folder

```
chatbot-skripsi/
├── app.py                          # Entry point utama aplikasi Streamlit
├── requirements.txt                # Daftar dependensi Python
├── .env                            # API key (tidak di-commit)
├── .gitignore
│
├── Data/
│   └── Dokumen_LayananPublik.pdf   # Basis pengetahuan dokumen resmi Dukcapil
│
├── assets/
│   ├── logo_dki.jpeg               # Logo DKI Jakarta
│   ├── kepala_dinas.jpeg           # Foto Kepala Dinas
│   └── struktur_organisasi.jpeg    # Bagan struktur organisasi
│
└── frontend/
    └── styles.py                   # Konfigurasi CSS dan styling UI
```

---

## ⚙️ Teknologi yang Digunakan

| Komponen | Teknologi |
|---|---|
| UI Framework | Streamlit |
| RAG Framework | LlamaIndex |
| LLM | `llama-3.1-8b-instant` via Groq API |
| Embedding Model | `BAAI/bge-small-en-v1.5` (HuggingFace) |
| Evaluasi | RAGAS |
| Bahasa | Python 3.10+ |

---

## 🚀 Cara Menjalankan

### 1. Clone repositori

```bash
git clone https://github.com/firmantmtm09/chatbot-skripsi.git
cd chatbot-skripsi
```

### 2. Buat virtual environment

```bash
python -m venv env
source env/bin/activate        # Linux/Mac
env\Scripts\activate           # Windows
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
```

### 4. Buat file `.env` dan isi API key

```
GROQ_API_KEY=your_groq_api_key_here
```

> Dapatkan Groq API key gratis di [console.groq.com](https://console.groq.com)

### 5. Jalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser pada `http://localhost:8501`

---

## 💬 Fitur Aplikasi

- **Asisten Virtual** — Chatbot di sidebar kanan yang menjawab pertanyaan seputar layanan Dukcapil DKI Jakarta
- **Berbasis Dokumen Resmi** — Jawaban diambil langsung dari dokumen PDF resmi, bukan dari pengetahuan umum model
- **Navigasi Informasi** — Tab Beranda, Profil, Layanan Online, Regulasi, dan Kontak Kami
- **Profil Dinas** — Informasi lengkap tentang tugas, fungsi, dan struktur organisasi Dukcapil DKI Jakarta
- **Kontak & Lokasi** — Jam operasional, WhatsApp pengaduan, email, dan peta lokasi kantor

---

## 📊 Evaluasi

Sistem dievaluasi menggunakan framework **RAGAS** dengan metrik:
- `Faithfulness` — seberapa setia jawaban terhadap dokumen sumber
- `Answer Relevancy` — seberapa relevan jawaban dengan pertanyaan
- `Context Precision` — ketepatan konteks yang diambil
- `Context Recall` — kelengkapan konteks yang diambil

Hasil evaluasi tersimpan di `backend/evaluasi_ragas_final.csv` dan `backend/rekap_evaluasi_ragas.xlsx`.

---

## 🔒 Catatan Keamanan

- Jangan commit file `.env` yang berisi API key
- File `.env` sudah terdaftar di `.gitignore`
- Ganti nilai `GROQ_API_KEY` di `app.py` dengan referensi ke variabel environment

---

## 👤 Author

**Firman Tamtama**  
Skripsi — Sistem Informasi  
Universitas Gunadarma · 2026

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik. Seluruh informasi layanan bersumber dari situs resmi [Dukcapil DKI Jakarta](https://dukcapil.jakarta.go.id).