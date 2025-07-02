<<<<<<< HEAD
#  PDF Q&A Bot (Watsonx.ai + HuggingFace + FAISS)

A Streamlit-based AI assistant that allows you to upload a PDF and ask questions about its content. It uses IBM Watsonx.ai LLM for answering questions, HuggingFace embeddings for semantic understanding, and FAISS for efficient document retrieval.

---

##  Features

-  Upload and read any PDF
-  Chunk PDF text and create embeddings
-  Retrieve relevant sections using FAISS
-  Answer questions using IBM Watsonx.ai's Granite model
-  Simple and responsive Streamlit UI

---

## 🛠️ Tech Stack

- **Streamlit** – Frontend interface  
- **PyMuPDF (`fitz`)** – PDF text extraction  
- **LangChain** – Document processing and chaining  
- **HuggingFace Embeddings** – `all-MiniLM-L6-v2` model  
- **FAISS** – Vector similarity search  
- **Watsonx.ai** – LLM for final answer generation

---

##  Requirements

Install all dependencies using:

```bash
pip install -r requirements.txt
=======
# PDF-Q-A-BOT
A Streamlit app to ask questions from any uploaded PDF using OpenAI.
>>>>>>> 2d16c3d86459cdbccbfcee233b748b905f7c9f26
