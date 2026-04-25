from dotenv import load_dotenv
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

print("📚 RAG Book Assistant")
print("=" * 50)

pdf_path = input("\nEnter PDF file path (or press Enter to skip): ").strip()

if pdf_path and os.path.exists(pdf_path):
    file_path = pdf_path
    print("✓ PDF file found!")

    create = input("Create vector database? (y/n): ").strip().lower()

    if create == 'y':
        print("\nProcessing document...")

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(docs)

        embeddings = MistralAIEmbeddings(
            model="mistral-embed-2312"
            )

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="chroma_db"
        )

        vectorstore.persist()

        print("✓ Vector database created!")

elif pdf_path:
    print(f"Error: PDF file not found at '{pdf_path}'")



if os.path.exists("chroma_db"):

    embeddings =  MistralAIEmbeddings(
    model="mistral-embed-2312"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":4,
            "fetch_k":10,
            "lambda_mult":0.5
        }
    )

    llm = ChatMistralAI(model="mistral-small-2506")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
            ),
            (
                "human",
                """Context:
{context}

Question:
{question}
"""
            )
        ]
    )

    print("\n" + "=" * 50)
    print("Ask Questions From the PDF")
    print("(Type 'exit' to quit)")
    print("=" * 50)

    while True:
        query = input("\nYour question: ").strip()

        if query.lower() == 'exit':
            print("\nGoodbye!")
            break

        if query:
            print("\nSearching...")

            docs = retriever.invoke(query)

            context = "\n\n".join(
                [doc.page_content for doc in docs]
            )

            final_prompt = prompt.invoke({
                "context": context,
                "question": query
            })

            response = llm.invoke(final_prompt)

            print("\n### AI Answer:")
            print(response.content)
else:
    print("\nNo vector database found. Please create one first by providing a PDF file.")
