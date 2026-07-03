import os
import re
import pandas as pd
from langchain_groq import ChatGroq

print("==================================================")
print("PROSES EVALUASI METRIK RAGAS (FIXED ACTIVE MODEL)...")
print("==================================================")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "evaluasi_ragas_final.csv")

if not os.path.exists(file_path):
    print(f"⚠️ Error: File '{file_path}' tidak ditemukan!")
    exit()

df = pd.read_csv(file_path)

os.environ["GROQ_API_KEY"] = "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"
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

faithfulness_scores = []
answer_relevance_scores = []
context_precision_scores = []

print(f"Total data ditemukan: {len(df)} baris. Mulai menilai secara objektif...")

for index, row in df.iterrows():
    q = row['question']
    a = row['answer']
    c = row['contexts']
    gt = row['ground_truth']
    
    prompt = f"""
    Bertindaklah sebagai ahli evaluator sistem RAG. Berikan nilai antara 0.0 hingga 1.0 untuk tiga metrik berikut berdasarkan data yang diberikan.
    
    DATA:
    - Pertanyaan: {q}
    - Jawaban Chatbot: {a}
    - Konteks Retrived: {c}
    - Ground Truth (Kunci Jawaban): {gt}
    
    METRIK YANG HARUS DINILAI:
    1. faithfulness: Apakah informasi di 'Jawaban Chatbot' sesuai dengan 'Konteks Retrived'? (1.0 jika sangat sesuai/tidak halusinasi, 0.0 jika mengada-ada).
    2. answer_relevance: Apakah 'Jawaban Chatbot' relevan menjawab 'Pertanyaan'? (1.0 jika sangat relevan, 0.0 jika tidak nyambung).
    3. context_precision: Apakah 'Konteks Retrived' relevan untuk menjawab 'Ground Truth'? (1.0 jika sangat presisi, 0.0 jika tidak membantu).
    
    Format output yang wajib Anda tulis adalah seperti contoh di bawah ini (tuliskan baris skornya saja):
    FAITHFULNESS: 0.95
    ANSWER_RELEVANCE: 0.80
    CONTEXT_PRECISION: 0.90
    """
    
    try:
        response = llm.invoke(prompt).content
        
        # Ekstrak nilai angka menggunakan Regular Expression
        f_match = re.search(r"FAITHFULNESS:\s*([\d\.]+)", response, re.IGNORECASE)
        a_match = re.search(r"ANSWER_RELEVANCE:\s*([\d\.]+)", response, re.IGNORECASE)
        c_match = re.search(r"CONTEXT_PRECISION:\s*([\d\.]+)", response, re.IGNORECASE)
        
        f_val = float(f_match.group(1)) if f_match else 0.0
        a_val = float(a_match.group(1)) if a_match else 0.0
        c_val = float(c_match.group(1)) if c_match else 0.0
        
        faithfulness_scores.append(f_val)
        answer_relevance_scores.append(a_val)
        context_precision_scores.append(c_val)
        
        print(f"-> Baris [{index+1}/{len(df)}] Sukses | F: {f_val} | A: {a_val} | C: {c_val}")
        
    except Exception as e:
        print(f"-> Baris [{index+1}/{len(df)}] Gagal. Error: {e}")
        faithfulness_scores.append(0.0)
        answer_relevance_scores.append(0.0)
        context_precision_scores.append(0.0)

df['faithfulness'] = faithfulness_scores
df['answer_relevance'] = answer_relevance_scores
df['context_precision'] = context_precision_scores

print("\n=== HASIL EVALUASI RAGAS REAL ===")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df[['question', 'faithfulness', 'answer_relevance', 'context_precision']])

output_eval = os.path.join(BASE_DIR, "evaluasi_ragas_final.csv")
df.to_csv(output_eval, index=False)

print("\n=======================================")
print("BERHASIL SELESAI DENGAN DATA VARIATIF!")
print(f"File nilai asli disimpan di: {output_eval}")
print("=======================================")