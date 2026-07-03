import os
import sys
import pandas as pd
import subprocess
import requests  
import time  

print("==================================================")
print("PROSES GENERATE DATA JAWABAN CHATBOT DUKCAPIL (FIXED PDF)...")
print("==================================================")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

questions = [
    "Apa syarat penerbitan kembali KK karena rusak atau hilang?",
    "Apa saja persyaratan dokumen untuk melakukan pindah datang ke DKI Jakarta?",
    "Bagaimana prosedur pengurusan pindah datang di Kelurahan tujuan?",
    "Apa saja persyaratan pencatatan kelahiran WNI yang terintegrasi dengan faskes?",
    "Siapa nama Kepala Dinas Kependudukan dan Pencatatan Sipil Provinsi DKI Jakarta saat ini?",
    "Apa saja syarat untuk melakukan pencatatan perkawinan bagi sesama WNI?",
    "Apa syarat melakukan pencatatan perceraian bagi penduduk WNI?",
    "Bagaimana syarat menerbitkan kembali kutipan akta pencatatan sipil yang rusak atau hilang?",
    "Berapa batas maksimal lembar fotokopi dokumen kependudukan untuk proses legalisasi?",
    "Melalui situs web apa permohonan daring dokumen administrasi kependudukan dkk Jakarta diajukan?",
    "Apa syarat pembuatan KTP-el baru bagi pemula yang berusia 17 tahun?",
    "Apa syarat penerbitan KTP-el baru bagi pemula di bawah 17 tahun yang sudah menikah?",
    "Berapa tarif atau biaya untuk pengurusan pindah datang dan pembuatan KTP-el?",
    "Apa saja syarat pelaporan pencatatan perubahan akta pencatatan sipil?",
    "Apa syarat pengurusan surat keterangan belum kawin secara daring?",
    "Apa saja syarat dokumen untuk pelaporan perjanjian perkawinan?",
    "Apa persyaratan untuk melakukan legalisasi dokumen kependudukan yang belum digital?",
    "Apa saja syarat pelaporan pencatatan pembetulan akta pencatatan sipil?",
    "Berapa jangka waktu maksimal pembuatan atau penerbitan KTP-el baru sejak syarat terpenuhi?",
    "Apa syarat pencatatan kelahiran bagi penduduk orang asing?"
]

ground_truths = [
    "Surat keterangan hilang dari kepolisian (jika hilang) atau membawa KK yang rusak (jika rusak), serta KTP-el.",
    "Surat Keterangan Pindah dari daerah asal, Biodata Penduduk, Surat Pernyataan Jaminan Tempat Tinggal dari Pemilik Rumah/Pengelola Rusun/Apartemen jika menumpang, KK dan KTP Penjamin jika menumpang, fotokopi Akta Kelahiran, serta fotokopi Akta Perkawinan/Surat Nikah atau akta perceraian jika berstatus kawin/cerai hidup.",
    "Pemohon mengambil nomor antrian di Loket Dukcapil Kelurahan, menyerahkan berkas lengkap, petugas memproses verifikasi dan memberikan bukti permohonan, memproses pengantar Surat Keterangan Pindah datang, lalu petugas mengajukan proses ke Sudin Dukcapil untuk memproses KK dan KTP baru.",
    "Surat Keterangan peristiwa kelahiran, fotokopi Surat Nikah/Akta Perkawinan orang tua atau SPTJM, serta fotokopi KK dan KTP-el orang tua.",
    "Denny Wahyu Haryanto.",
    "Fotokopi surat keterangan telah terjadinya perkawinan dari pemuka agama atau penghayat kepercayaan terhadap Tuhan YME, pas foto berwarna suami dan istri berdampingan ukuran 4x6 sebanyak 2 lembar, KTP-el dan KK asli, serta fotokopi akta perceraian/akta kematian jika berstatus cerai.",
    "Fotokopi salinan putusan pengadilan yang telah mempunyai kekuatan hukum tetap, kutipan akta perkawinan asli, KTP-el asli, dan KK asli.",
    "Surat pernyataan rusak/hilang dari yang bersangkutan atau Surat keterangan kehilangan dari Kepolisian setempat, fotokopi kutipan Akta Pencatatan Sipil yang hilang atau kutipan akta asli yang rusak, serta fotokopi KK dan KTP-el.",
    "Maksimal 11 lembar fotokopi.",
    "Melalui website resmi alpukat-dukcapil.jakarta.go.id.",
    "Fotokopi Kartu Keluarga (KK).",
    "KK asli dan fotokopi Surat Nikah/Akta Perkawinan.",
    "Gratis atau tidak dipungut biaya.",
    "Fotokopi Penetapan Pengadilan Negeri yang telah dilegalisir, Kutipan Akta Asli, Fotokopi KTP & KK DKI Jakarta, Surat Pernyataan Bermeterai Pembaharuan Kutipan Akta, serta Surat Kuasa Bermeterai jika diwakilkan.",
    "Fotokopi Kutipan Akta Kelahiran, Surat Keterangan dari Kelurahan (PM1), asli dan fotokopi KK dan KTP, serta Surat Pernyataan Belum Pernah Menikah Bermeterai.",
    "Fotokopi KK & KTP DKI Jakarta suami & istri, fotokopi ITAP/ITAS dan Paspor bagi orang asing, asli dan fotokopi Kutipan Akta Perkawinan, asli dan fotokopi Perjanjian Perkawinan dari Notaris yang dilegalisir, Surat Pernyataan Kedua Pasangan bermeterai, serta Surat Kuasa bermeterai jika diwakilkan.",
    "Fotokopi dokumen kependudukan yang akan dilegalisasi.",
    "Fotokopi KK & KTP, asli dan fotokopi Kutipan Akta Pencatatan Sipil, serta Dokumen Autentik Pendukung Pembetulan Akta Pencatatan Sipil.",
    "Selambat-lambatnya 14 hari.",
    "Surat Keterangan Peristiwa Kelahiran dari Dokter/RS, fotokopi Akta Perkawinan Orang Tua (terjemahan jika bahasa asing), fotokopi Identitas Orang Tua (KTP/KK/VISA/SKTT/ITAP), Dokumen Perjalanan/Paspor, serta Identitas 2 Orang Saksi."
]

pdf_path = os.path.join(BASE_DIR, "Data", "Dokumen_LayananPublik.pdf")
if not os.path.exists(pdf_path):
    pdf_path = os.path.join(BASE_DIR, "..", "Data", "Dokumen_LayananPublik.pdf")

paragraphs = []
if os.path.exists(pdf_path):
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        paragraphs = [p.strip() for p in full_text.split("\n") if len(p.strip()) > 20]
    except Exception as e:
        print(f"⚠️ Gagal membaca PDF: {e}")

API_URL = "http://127.0.0.1:8000/chat"
test_data = []

print("Memulai pengambilan jawaban baru dari local API...")
for i, (question, ground_truth) in enumerate(zip(questions, ground_truths), start=1):
    try:
        response = requests.post(API_URL, json={"message": question}, timeout=60)
        answer = response.json().get("reply", "Tidak ada balasan.") if response.status_code == 200 else "Error API"
        
        matched_context = ""
        keywords = [w for w in question.split() if len(w) > 4]
        for p in paragraphs:
            if any(k.lower() in p.lower() for k in keywords[:2]):
                matched_context += p + " "
                if len(matched_context) > 300:
                    break
        
        if not matched_context:
            matched_context = "Dokumen Panduan Standar Pelayanan Kependudukan Dinas Dukcapil DKI Jakarta."

        test_data.append({
            "question": question,
            "answer": answer.replace('"', "'"), 
            "contexts": matched_context.strip().replace('"', "'"),
            "ground_truth": ground_truth
        })
        print(f"-> Berhasil memproses baris [{i}/{len(questions)}]")
        time.sleep(1)
    except Exception as e:
        test_data.append({"question": question, "answer": "Error", "contexts": "Error", "ground_truth": ground_truth})

df = pd.DataFrame(test_data)
output_file = os.path.join(BASE_DIR, "evaluasi_ragas_final.csv")
df.to_csv(output_file, index=False)

print("\n=======================================")
print("FILE CSV BERHASIL DIPERBARUI SECARA BERSIH!")
print("=======================================")

print("\n>>> Menjalankan proses perhitungan metrik...")
try:
    eval_script = os.path.join(BASE_DIR, "evaluasi_ragas.py")
    subprocess.run(["python3", eval_script], check=True)
except Exception as e:
    print(f"Pemicuan evaluasi otomatis: {e}")