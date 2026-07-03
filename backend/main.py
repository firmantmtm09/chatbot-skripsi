import os
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.groq import Groq
from fastapi.middleware.cors import CORSMiddleware

os.environ["GROQ_API_KEY"] = "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"

Settings.llm = Groq(model="llama-3.1-8b-instant")

from llama_index.core.embeddings import MockEmbedding
Settings.embed_model = MockEmbedding(embed_dim=768)

query_engine = None

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, "Data")
    
    if not os.path.exists(data_path):
        data_path = os.path.join(BASE_DIR, "..", "Data")
        
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Folder 'Data' tidak ditemukan di {os.path.abspath(data_path)}")

    documents = SimpleDirectoryReader(data_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    
    template = PromptTemplate(
        "Anda adalah Virtual Assistant resmi Dukcapil DKI Jakarta. Gunakan bahasa yang sopan, ramah, dan formal.\n"
        "Tugas Anda adalah memberikan informasi akurat mengenai syarat layanan dokumen kependudukan.\n\n"
        "ATURAN UTAMA:\n"
        "1. Utamakan mencari jawaban dari Context Dokumen yang disediakan.\n"
        "2. PENTING: Jika informasi di dalam dokumen terpotong, gantung, atau tidak lengkap (seperti pada bagian 'Persyaratan Pembuatan KTP-el Baru'), "
        "GUNAKAN pengetahuan internal Anda untuk melengkapi jawaban secara benar dan logis bagi warga DKI Jakarta "
        "(yaitu: Berusia minimal 17 tahun atau sudah pernah menikah, serta membawa fotokopi Kartu Keluarga (KK)).\n"
        "3. JANGAN PERNAH memberikan syarat 'Surat Kematian' atau 'Akte Kematian' jika user bertanya tentang pembuatan E-KTP baru!\n\n"
        "Context Dokumen:\n{context_str}\n\n"
        "Pertanyaan User: {query_str}\n"
        "Jawaban Resmi Virtual Assistant:"
    )
    
    query_engine = index.as_query_engine(text_qa_template=template, similarity_top_k=3)
    print("✅ RAG / KNOWLEDGE BASE BERHASIL AKTIF INSTAN!")
    print(f"📁 Menggunakan data riel dari folder: {os.path.abspath(data_path)}")
except Exception as e:
    print(f"⚠️ Warning: Gagal memuat data: {e}")

app = FastAPI(title="Dukcapil Chatbot API Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    global query_engine
    if query_engine:
        try:
            response = query_engine.query(req.message)
            return {"status": "success", "reply": str(response)}
        except Exception as e:
            return {"status": "error", "reply": f"Maaf, server AI sedang sibuk. (Error: {e})"}
    else:
        return {"status": "error", "reply": "Maaf, sistem basis data belum siap."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)