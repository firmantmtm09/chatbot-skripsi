import os
import re
import time
import pandas as pd
from langchain_groq import ChatGroq

GROQ_API_KEY = "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"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "evaluasi_ragas_final.csv")
df = pd.read_csv(file_path)

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=GROQ_API_KEY)
results = []

for index, row in df.iterrows():
    q, a, gt = row['question'], row['answer'], row['ground_truth']
    
    prompt = f"""
    Evaluasi sistem RAG berdasarkan metrik berikut (skala 0.0 - 1.0):
    Pertanyaan: {q}
    Jawaban Sistem: {a}
    Jawaban Benar (Ground Truth): {gt}
    
    1. faithfulness: Apakah Jawaban Sistem akurat (1.0 = akurat, 0.0 = halusinasi)
    2. answer_relevance: Apakah Jawaban Sistem menjawab pertanyaan?
    3. context_precision: Apakah informasi yang diberikan presisi?
    
    Tuliskan dalam format:
    FAITHFULNESS: <nilai>
    ANSWER_RELEVANCE: <nilai>
    CONTEXT_PRECISION: <nilai>
    """
    
    try:
        response = llm.invoke(prompt).content
        f_val = float(re.search(r"FAITHFULNESS:\s*([\d\.]+)", response, re.IGNORECASE).group(1))
        a_val = float(re.search(r"ANSWER_RELEVANCE:\s*([\d\.]+)", response, re.IGNORECASE).group(1))
        c_val = float(re.search(r"CONTEXT_PRECISION:\s*([\d\.]+)", response, re.IGNORECASE).group(1))
        results.append({'faithfulness': f_val, 'answer_relevance': a_val, 'context_precision': c_val})
        print(f"-> Baris {index+1} sukses")
        time.sleep(0.5)
    except:
        results.append({'faithfulness': 0.0, 'answer_relevance': 0.0, 'context_precision': 0.0})

eval_df = pd.DataFrame(results)
df = pd.concat([df.reset_index(drop=True), eval_df], axis=1)
df.to_csv(file_path, index=False)