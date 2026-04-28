import os
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import Config
import shutil

def get_vectorstore():
    if not check_db_exists():
        return None

    embeddings = MistralAIEmbeddings(model=Config.EMBEDDING_MODEL)
    vectorstore = Chroma(
        persist_directory=Config.CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="pdf_collection"
    )
    return vectorstore

def check_db_exists():
    return os.path.exists(Config.CHROMA_PERSIST_DIR)

def clear_database():
    if check_db_exists():
        shutil.rmtree(Config.CHROMA_PERSIST_DIR)
        return True
    return False
