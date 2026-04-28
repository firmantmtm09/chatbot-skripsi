import streamlit as st
import os

st.set_page_config(page_title="Bot Layanan Publik", layout="centered")

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

os.environ["GROQ_API_KEY"] = "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"

Settings.llm = Groq(model="llama-3.1-8b-instant")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

st.title("🤖 Chatbot Informasi KK")
st.markdown("---")

@st.cache_resource(show_spinner="Sedang memuat dokumen... tunggu ya ⏳")
def prepare_data():
    reader = SimpleDirectoryReader(input_dir="./Data")
    documents = reader.load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index

try:
    with st.spinner("Memuat dokumen dan AI model... ini mungkin 1-2 menit pertama kali"):
        index = prepare_data()

    st.success("✅ Dokumen siap! Silakan mulai bertanya.")
    
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt="Kamu adalah asisten layanan publik yang ramah. Jawablah hanya berdasarkan dokumen yang diberikan. Jawab dalam Bahasa Indonesia."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Tanya soal KK..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Sedang mencari jawaban..."):
            response = chat_engine.chat(prompt)

        with st.chat_message("assistant"):
            st.markdown(response.response)
        st.session_state.messages.append({"role": "assistant", "content": response.response})

except Exception as e:
    st.error(f"❌ Error: {e}")