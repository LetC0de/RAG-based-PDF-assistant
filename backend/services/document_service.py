import os
import time
import shutil
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import Config

def process_pdf(file_path):
    start_time = time.time()

    # Delete existing database completely to avoid readonly errors
    if os.path.exists(Config.CHROMA_PERSIST_DIR):
        try:
            shutil.rmtree(Config.CHROMA_PERSIST_DIR)
            print("Successfully deleted existing database")
        except Exception as e:
            print(f"Error deleting database: {e}")
            # If we can't delete, create with unique collection name
            pass

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    embeddings = MistralAIEmbeddings(model=Config.EMBEDDING_MODEL)

    # Use a fixed collection name (will be replaced each time)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=Config.CHROMA_PERSIST_DIR,
        collection_name="pdf_collection"
    )

    # Don't call persist() - it's deprecated and auto-persists anyway

    processing_time = time.time() - start_time

    return {
        "chunks_created": len(chunks),
        "processing_time": f"{processing_time:.1f}s"
    }
