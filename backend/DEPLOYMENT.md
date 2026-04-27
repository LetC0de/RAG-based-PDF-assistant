# RAG Backend API

Flask REST API backend for the RAG (Retrieval-Augmented Generation) application.

## 📁 Project Structure

```
backend/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in git)
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── services/
│   ├── __init__.py
│   ├── document_service.py         # PDF processing & ingestion
│   ├── query_service.py            # Question answering logic
│   └── vectorstore_service.py      # Chroma DB management
├── routes/
│   ├── __init__.py
│   ├── document_routes.py          # Document upload endpoints
│   └── query_routes.py             # Query endpoints
├── utils/
│   ├── __init__.py
│   └── response.py                 # Standardized JSON responses
├── chroma_db/                      # Vector database (auto-created)
└── uploads/                        # Temporary uploads (auto-created)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your Mistral API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

### 3. Run the Server

```bash
python app.py
```

Server will start on `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```bash
GET /api/health
```

### Upload PDF Document
```bash
POST /api/documents/upload
Content-Type: multipart/form-data

Body: file (PDF, max 50MB)
```

### Query Document
```bash
POST /api/query
Content-Type: application/json

Body: {"question": "Your question here"}
```

### Delete Vector Database
```bash
DELETE /api/documents
```

## 🔧 Configuration

Edit `config.py` to customize:

- `EMBEDDING_MODEL` - Mistral embedding model
- `LLM_MODEL` - Mistral chat model
- `CHUNK_SIZE` - Text chunk size (default: 1000)
- `CHUNK_OVERLAP` - Chunk overlap (default: 200)
- `RETRIEVER_K` - Number of chunks to retrieve (default: 4)
- `MAX_FILE_SIZE` - Max upload size (default: 50MB)

## 🌐 Deployment

### Option 1: Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t rag-backend .
docker run -p 5000:5000 --env-file .env rag-backend
```

### Option 2: Production Server (Gunicorn)

Install gunicorn:
```bash
pip install gunicorn
```

Run:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Cloud Platforms

**Heroku:**
```bash
heroku create your-app-name
heroku config:set MISTRAL_API_KEY=your_key
git push heroku main
```

**Railway/Render:**
- Connect your GitHub repo
- Set environment variable: `MISTRAL_API_KEY`
- Deploy automatically

## 🔒 Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Use environment variables for API keys
- Enable HTTPS in production
- Consider adding rate limiting
- Add authentication for production use

## 📊 Tech Stack

- **Framework:** Flask 3.0.0
- **Vector DB:** ChromaDB 1.5.8
- **LLM:** Mistral AI (mistral-small-2506)
- **Embeddings:** Mistral AI (mistral-embed-2312)
- **RAG Framework:** LangChain 1.2.15

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

**CORS errors:**
- CORS is already enabled for all origins
- For production, restrict origins in `app.py`

**Mistral API errors:**
- Check your API key in `.env`
- Verify API key has credits

## 📝 Error Codes

- `VECTOR_DB_NOT_FOUND` - No database, upload PDF first
- `INVALID_FILE_TYPE` - Only PDF files allowed
- `FILE_TOO_LARGE` - File exceeds 50MB
- `MISTRAL_API_ERROR` - Mistral API call failed
- `PROCESSING_ERROR` - Document processing failed
- `INVALID_REQUEST` - Missing required fields

## 📄 License

MIT
