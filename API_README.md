# RAG Flask Backend API

Flask REST API backend for the RAG (Retrieval-Augmented Generation) application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure `.env` file contains your Mistral API key:
```
MISTRAL_API_KEY=your_key_here
```

3. Start the server:
```bash
python app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### 1. Health Check
```bash
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "vector_db_exists": true,
    "mistral_api_configured": true
  }
}
```

### 2. Upload PDF Document
```bash
POST /api/documents/upload
Content-Type: multipart/form-data
```

**Request:**
- `file`: PDF file (max 50MB)

**Response:**
```json
{
  "success": true,
  "message": "Document processed successfully",
  "data": {
    "filename": "deeplearning.pdf",
    "chunks_created": 1146,
    "processing_time": "34.6s"
  }
}
```

### 3. Query Document
```bash
POST /api/query
Content-Type: application/json
```

**Request:**
```json
{
  "question": "What is deep learning?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "question": "What is deep learning?",
    "answer": "Deep learning is a subset of machine learning...",
    "sources": [
      {
        "content": "...",
        "page": 56
      }
    ]
  }
}
```

### 4. Delete Vector Database
```bash
DELETE /api/documents
```

**Response:**
```json
{
  "success": true,
  "message": "Vector database cleared successfully"
}
```

## Testing Examples

```bash
# Health check
curl http://localhost:5000/api/health

# Upload PDF
curl -X POST -F "file=@deeplearning.pdf" http://localhost:5000/api/documents/upload

# Ask question
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is deep learning?"}'

# Delete database
curl -X DELETE http://localhost:5000/api/documents
```

## Project Structure

```
RAG/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration management
├── services/
│   ├── document_service.py         # PDF processing & ingestion
│   ├── query_service.py            # Question answering logic
│   └── vectorstore_service.py      # Chroma DB management
├── routes/
│   ├── document_routes.py          # Document upload endpoints
│   └── query_routes.py             # Query endpoints
├── utils/
│   └── response.py                 # Standardized JSON responses
├── RagUI.py                        # Original CLI version
└── chroma_db/                      # Vector database storage
```

## Error Codes

- `VECTOR_DB_NOT_FOUND` - No vector database exists, upload a PDF first
- `INVALID_FILE_TYPE` - Only PDF files are allowed
- `FILE_TOO_LARGE` - File exceeds 50MB limit
- `MISTRAL_API_ERROR` - Mistral API call failed
- `PROCESSING_ERROR` - Document processing failed
- `INVALID_REQUEST` - Missing required fields

## Notes

- The backend maintains the same RAG logic as the CLI version
- CORS is enabled for frontend integration
- Uploaded files are temporarily stored and deleted after processing
- Vector database is persisted to disk in `chroma_db/` directory
