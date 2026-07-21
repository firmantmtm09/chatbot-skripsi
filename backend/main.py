import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import TokenTextSplitter

GROQ_API_KEY = "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"

Settings.llm = Groq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=50)

query_engine = None

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, "Data")
    
    if not os.path.exists(data_path):
        data_path = os.path.join(BASE_DIR, "..", "Data")
        
    documents = SimpleDirectoryReader(data_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    
    template = PromptTemplate(
        "Anda adalah Virtual Assistant resmi Dukcapil DKI Jakarta. Gunakan bahasa yang sopan, ramah, dan formal.\n"
        "Tugas Anda adalah memberikan informasi akurat mengenai syarat layanan dokumen kependudukan.\n\n"
        "ATURAN UTAMA:\n"
        "1. Utamakan mencari jawaban dari Context Dokumen yang disediakan.\n"
        "2. Jika informasi tidak lengkap dalam dokumen, berikan jawaban berdasarkan basis pengetahuan umum yang valid.\n"
        "3. JANGAN PERNAH memberikan syarat yang tidak sesuai atau menyesatkan.\n\n"
        "Context Dokumen:\n{context_str}\n\n"
        "Pertanyaan User: {query_str}\n"
        "Jawaban Resmi Virtual Assistant:"
    )
    
    query_engine = index.as_query_engine(text_qa_template=template, similarity_top_k=4)
    print("✅ Sistem RAG berhasil diinisialisasi dengan Groq API.")

except Exception as e:
    print(f"⚠️ Error pada inisialisasi sistem: {e}")

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
            return {"status": "error", "reply": f"Maaf, terjadi kesalahan teknis: {e}"}
    return {"status": "error", "reply": "Maaf, basis data belum siap."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)