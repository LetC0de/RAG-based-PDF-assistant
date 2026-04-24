# 📄 RAG-based PDF Assistant – Intelligent Document QA System

RAG-based PDF Assistant is a Streamlit-powered application that allows users to upload PDF documents and ask questions based on their content. It uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers using Mistral embeddings and a Chroma vector database.


## 🚀 Features

* 📂 Upload any PDF document
* ✂️ Automatic text chunking for better retrieval
* 🧠 Semantic search using vector embeddings
* 🔍 Context-aware question answering (RAG pipeline)
* 🤖 AI responses powered by Mistral LLM
* 💾 Persistent vector database using Chroma
* ⚡ Fast and interactive UI with Streamlit


## 🧠 Tech Stack

* Python
* Streamlit
* LangChain
* Mistral AI (LLM + Embeddings model)
* ChromaDB (Vector Store)
* PyPDF (PDF Loader)
* Retriever
* dotenv


## Full RAG Flow (End-to-End)


User uploads PDF
        ↓
PyPDFLoader → Extract text
        ↓
Text Splitter → Create chunks
        ↓
Embeddings → Convert to vectors
        ↓
ChromaDB → Store vectors
        ↓
User asks question
        ↓
Retriever → Find relevant chunks
        ↓
Prompt Template → Build context
        ↓
Mistral LLM → Generate answer
        ↓
Streamlit UI → Display response



## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/LetC0de/RAG-based-PDF-assistant.git
cd RAG
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```


## 🔐 Environment Variables

Create a `.env` file in the root directory:

```
MISTRAL_API_KEY=your_mistral_api_key
```

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run RagUI.py
```

## 🛠️ How It Works

1. Upload a PDF file
2. The document is:

   * Loaded using PyPDFLoader
   * Split into chunks
   * Converted into embeddings
3. Chunks are stored in Chroma vector database
4. On user query:

   * Relevant chunks are retrieved
   * Context is passed to Mistral LLM
   * AI generates answer based only on document


## 📁 Project Structure

```
rag-pdf-assistant/
│
├── RagUI.py
├── chroma_db/
├── .env
├── .gitignore
└── README.md
```

## ⚠️ Notes

* Ensure your Mistral API key is valid
* `.env` file is ignored using `.gitignore`
* Do not upload sensitive documents
* First run may take time to create vector database


## 👨‍💻 Author

Abhishek Nishad

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
