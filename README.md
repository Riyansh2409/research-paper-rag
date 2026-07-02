# 🤖 AI Research Paper Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Gemini](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-orange)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-blueviolet)

An AI-powered Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF research papers and interact with them using Google's Gemini 2.5 Flash model.

The application extracts text from uploaded PDFs, converts them into vector embeddings, stores them in a FAISS vector database, retrieves the most relevant information for each query, and generates context-aware answers with source citations.

---

## ✨ Features

- 📄 Upload multiple PDF documents
- 🤖 Chat with PDFs using Gemini 2.5 Flash
- 🔍 Semantic similarity search using FAISS
- 🧠 Conversation memory
- 📚 Source citations for every response
- 📄 Retrieved chunk viewer
- ⚙️ Adjustable Top-K retrieval
- 📊 PDF statistics dashboard
- 📁 Uploaded document information
- 💾 Export chat history
- ⚡ Hash-based caching to avoid unnecessary reprocessing

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini 2.5 Flash
- FAISS Vector Store
- Sentence Transformers
- HuggingFace Embeddings
- PyPDF
- Python Dotenv

---

## 📁 Project Structure

```text
AI-Research-Paper-Assistant
│
├── data/
│
├── src/
│   ├── chains/
│   ├── chunking/
│   ├── embeddings/
│   ├── llm/
│   ├── loader/
│   ├── memory/
│   ├── prompts/
│   ├── retriever/
│   ├── utils/
│   └── vectorstore/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/Riyansh2409/research_paper_rag.git
```

### Move into the project

```bash
cd research_paper_rag
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Run the application

```bash
streamlit run app.py
```

---

## ⚙️ How It Works

1. Upload one or more PDF research papers.
2. PDFs are loaded using PyPDF.
3. Documents are split into semantic chunks.
4. Sentence Transformers generate embeddings.
5. FAISS indexes all document embeddings.
6. The retriever finds the most relevant chunks.
7. Retrieved context is combined with chat history.
8. Gemini 2.5 Flash generates the final answer.
9. Sources and retrieved chunks are displayed to improve transparency.

---

## 📌 Current Features

- ✅ Multi-PDF Support
- ✅ FAISS Vector Database
- ✅ Semantic Retrieval
- ✅ Configurable Top-K Retrieval
- ✅ Conversation Memory
- ✅ Source References
- ✅ Retrieved Chunk Viewer
- ✅ Chat Export
- ✅ PDF Statistics
- ✅ Uploaded Document Viewer
- ✅ Hash-Based Document Caching

---

## 🔮 Future Improvements

- Hybrid Search (BM25 + Dense Retrieval)
- Cross-Encoder Re-ranking
- OCR Support for Scanned PDFs
- Multi-Modal RAG
- Streaming Responses
- Cloud Deployment
- Authentication & User Accounts

---

## 👨‍💻 Author

**Riyansh Jain**

B.Tech Artificial Intelligence & Machine Learning

Jain University

GitHub: [Riyansh2409](https://github.com/Riyansh2409)

---

## ⭐ If you found this project useful, consider giving it a Star on GitHub!