# 📚 Chat With Your PDF — Powered by Watsonx.ai, HuggingFace, and FAISS

This is a Streamlit web application that lets you upload a PDF and ask questions about its contents.  
It extracts the PDF text, splits it into chunks, creates a vector database using Hugging Face embeddings + FAISS, and answers your queries using IBM Watsonx's Granite LLM.

---

## 🚀 Features

- Upload a PDF file and extract its text
- Split the document into context-aware chunks
- Generate embeddings using HuggingFace's `all-MiniLM-L6-v2`
- Perform similarity search with FAISS to find relevant chunks
- Ask natural language questions about the PDF content
- Get AI-powered answers from Watsonx.ai Granite model
- Optional debug mode to view extracted chunks

---

## 🔧 Tech Stack

- [Streamlit](https://streamlit.io/) — Frontend UI
- [IBM Watsonx.ai](https://www.ibm.com/watsonx) — LLM for generating answers
- [Hugging Face Transformers](https://huggingface.co/) — Text embeddings
- [FAISS](https://github.com/facebookresearch/faiss) — Vector search
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) — PDF text extraction
- [LangChain](https://www.langchain.com/) — Text splitting & vector store integration
- [dotenv](https://pypi.org/project/python-dotenv/) — Secure environment variable management

---

## 🔐 Setup: Environment Variables

Create a `.env` file in the project root and add:

```
IBM_API_KEY=your_ibm_api_key
PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   streamlit run app.py
   ```

   Replace `app.py` with your script name.

---

## 📂 Example Usage

1. Upload a PDF file.
2. Wait for it to process the text and build the vector store.
3. Type your question in the input box.
4. Get a context-relevant answer from the PDF.

---

## ✅ Example Questions

- "What is the purpose of this document?"
- "Summarize the first section."
- "What conclusions are mentioned?"
