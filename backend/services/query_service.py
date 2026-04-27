from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from config import Config
from services.vectorstore_service import get_vectorstore

def answer_question(question):
    vectorstore = get_vectorstore()

    if vectorstore is None:
        return None

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": Config.RETRIEVER_K,
            "fetch_k": Config.RETRIEVER_FETCH_K,
            "lambda_mult": Config.RETRIEVER_LAMBDA_MULT
        }
    )

    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    llm = ChatMistralAI(model=Config.LLM_MODEL)

    prompt = ChatPromptTemplate.from_messages([
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
    ])

    final_prompt = prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(final_prompt)

    sources = [
        {
            "content": doc.page_content,
            "page": doc.metadata.get("page", "unknown")
        }
        for doc in docs
    ]

    return {
        "question": question,
        "answer": response.content,
        "sources": sources
    }
