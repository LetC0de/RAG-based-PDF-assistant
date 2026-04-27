import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import Config

def process_pdf(file_path):
    start_time = time.time()

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    embeddings = MistralAIEmbeddings(model=Config.EMBEDDING_MODEL)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=Config.CHROMA_PERSIST_DIR
    )

    vectorstore.persist()

    processing_time = time.time() - start_time

    return {
        "chunks_created": len(chunks),
        "processing_time": f"{processing_time:.1f}s"
    }
