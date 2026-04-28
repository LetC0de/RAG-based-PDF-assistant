import os
import time
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import Config

def process_pdf(file_path):
    start_time = time.time()

    # Use ChromaDB's API to reset, not file deletion
    try:
        # Try to delete existing collection using ChromaDB API
        client = chromadb.PersistentClient(path=Config.CHROMA_PERSIST_DIR)

        try:
            client.delete_collection("pdf_collection")
            print("Deleted existing collection")
        except:
            print("No existing collection to delete")

    except Exception as e:
        print(f"Collection cleanup: {e}")

    # Load and process PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    embeddings = MistralAIEmbeddings(model=Config.EMBEDDING_MODEL)

    # Create new collection
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=Config.CHROMA_PERSIST_DIR,
        collection_name="pdf_collection"
    )

    processing_time = time.time() - start_time

    return {
        "chunks_created": len(chunks),
        "processing_time": f"{processing_time:.1f}s"
    }
