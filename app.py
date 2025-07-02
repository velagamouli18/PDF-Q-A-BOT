import streamlit as st
import fitz  # PyMuPDF
import os
import requests
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# ======= 🔐 Load Secrets from .env =======
load_dotenv()
IBM_API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")

# ======= 🧠 Watsonx LLM Call =======
def ask_watsonx(prompt, token):
    url = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-05-01"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": "ibm/granite-3-2-8b-instruct",
        "input": prompt,
        "project_id": PROJECT_ID,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print("🔁 Watsonx Response Status:", response.status_code)
    print("🔁 Watsonx Raw Response:", response.text)

    try:
        return response.json()['results'][0]['generated_text']
    except Exception:
        raise RuntimeError(f"❌ WatsonX API failed:\nStatus Code: {response.status_code}\nResponse:\n{response.text}")

# ======= 🔑 IBM Token Fetch =======
@st.cache_resource
def get_cached_token():
    return get_iam_token(IBM_API_KEY)

def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(url, headers=headers, data=data)

    if "access_token" not in response.json():
        st.error("❌ Failed to get IBM IAM token. Response:")
        st.code(response.text)
        raise RuntimeError("Token fetch failed.")

    return response.json()["access_token"]

# ======= 📄 PDF to Text =======
def extract_text(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ======= 🔍 Chunking =======
def get_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.create_documents([text])

# ======= 🧠 Embeddings + FAISS =======
def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_documents(docs, embeddings)

# ======= 🧠 RAG with Watsonx =======
def generate_answer(vectorstore, question, token):
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a helpful AI assistant. Use the context below to answer the user's question accurately.

Context:
{context}

Question:
{question}

Answer only using the provided context. If the answer is not available in the provided context, say:
"The answer is not available in the provided context."
    """.strip()

    print("🔎 Retrieved Context:\n", context)
    print("❓ User Question:", question)

    return ask_watsonx(prompt, token)

# ======= 🚀 Streamlit App =======
st.set_page_config(page_title="PDF Q&A", layout="wide")
st.title("📚 Chat With Your PDF (Watsonx.ai + HuggingFace + FAISS)")

pdf = st.file_uploader("Upload your PDF file here", type="pdf")

if pdf:
    st.info("⏳ Extracting text from PDF...")
    text = extract_text(pdf)

    docs = get_chunks(text)
    vectorstore = create_vector_store(docs)
    token = get_cached_token()

    st.success("✅ PDF processed and ready!")
    st.markdown("---")

    if st.checkbox("🔍 Show extracted chunks (debug)"):
        for i, doc in enumerate(docs[:5]):
            st.markdown(f"**Chunk {i+1}:**\n```\n{doc.page_content[:500]}\n```")

    question = st.text_input("Ask a question based on the PDF:")
    if question:
        with st.spinner("🔎 Getting your answer from Watsonx..."):
            try:
                answer = generate_answer(vectorstore, question, token)
                st.markdown("### 📥 Answer:")
                st.success(answer)
            except Exception as e:
                st.error("Something went wrong.")
                st.code(str(e))
