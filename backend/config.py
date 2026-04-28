from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    CHROMA_PERSIST_DIR = os.path.join("/tmp", "chroma_db")
    EMBEDDING_MODEL = "mistral-embed-2312"
    LLM_MODEL = "mistral-small-2506"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    RETRIEVER_K = 4
    RETRIEVER_FETCH_K = 10
    RETRIEVER_LAMBDA_MULT = 0.5
    UPLOAD_FOLDER = os.path.join("/tmp", "uploads")
    MAX_FILE_SIZE = 50 * 1024 * 1024
