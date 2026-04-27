# RAG Document Intelligence - Complete Project

A full-stack RAG (Retrieval-Augmented Generation) application for querying PDF documents using AI.

## 📁 Project Structure

```
RAG/
├── backend/                        # 🔧 Backend API (Ready for deployment)
│   ├── app.py                      # Flask application
│   ├── config.py                   # Configuration
│   ├── requirements.txt            # Dependencies
│   ├── .env                        # Environment variables (not in git)
│   ├── .env.example                # Environment template
│   ├── .gitignore                  # Git ignore rules
│   ├── README.md                   # Backend documentation
│   ├── DEPLOYMENT.md               # Deployment guide
│   ├── services/                   # Business logic
│   │   ├── document_service.py
│   │   ├── query_service.py
│   │   └── vectorstore_service.py
│   ├── routes/                     # API endpoints
│   │   ├── document_routes.py
│   │   └── query_routes.py
│   └── utils/                      # Helper functions
│       └── response.py
│
├── frontend/                       # 🎨 Frontend UI
│   ├── index.html                  # Main page
│   ├── style.css                   # Styles & animations
│   ├── script.js                   # Frontend logic
│   └── README.md                   # Frontend documentation
│
├── Rag.py                        # Original CLI version
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your MISTRAL_API_KEY
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend

Open `frontend/index.html` in your browser, or use a local server:

```bash
cd frontend
python -m http.server 8000
# Visit http://localhost:8000
```

## ✨ Features

### Backend API
- ✅ PDF document upload and processing
- ✅ Vector database creation with ChromaDB
- ✅ Question answering with Mistral AI
- ✅ MMR retrieval for relevant context
- ✅ RESTful API with CORS enabled
- ✅ Error handling and validation
- ✅ Health check endpoint

### Frontend UI
- ✅ Beautiful, refined light theme
- ✅ PDF upload with progress indicator
- ✅ Chat interface with message history
- ✅ Source citations with page numbers
- ✅ Real-time status updates
- ✅ Error handling UI
- ✅ Clear chat functionality
- ✅ Responsive design

## 🔧 Tech Stack

**Backend:**
- Flask 3.0.0
- ChromaDB 1.5.8
- LangChain 1.2.15
- Mistral AI (LLM & Embeddings)

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- Custom animations
- Fetch API for backend communication

## 📡 API Endpoints

- `GET /api/health` - Health check
- `POST /api/documents/upload` - Upload PDF
- `POST /api/query` - Ask questions
- `DELETE /api/documents` - Clear database

## 🌐 Deployment

The backend folder is ready for deployment to:
- Docker
- Heroku
- Railway
- Render
- Any cloud platform supporting Python/Flask

See `backend/DEPLOYMENT.md` for detailed instructions.

## 📝 Environment Variables

Create `backend/.env`:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

## 🎯 Usage Flow

1. Start the backend server
2. Open the frontend in browser
3. Upload a PDF document
4. Wait for processing (creates vector database)
5. Ask questions about the document
6. Get AI-generated answers with source citations

## 📚 Documentation

- Backend API: `backend/README.md`
- Deployment Guide: `backend/DEPLOYMENT.md`
- Frontend: `frontend/README.md`

## 🔒 Security

- API keys stored in `.env` (not committed)
- CORS enabled (restrict in production)
- File type validation
- File size limits (50MB)

## 📄 License

MIT

---

**Note:** The original CLI version (`RagUI.py`) is preserved for reference.
