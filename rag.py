import json

# from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

# from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import dotenv

# Load .env
dotenv.load_dotenv()

## Load vectorized data and initialize embeddings.
persist_directory = "data/vectordb"
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Define a prompt template for the RAG task, outlining how the context and question should be presented.
template = """You are an assistant for question-answering tasks regarding trending research (the context). Use the following pieces of context to answer the question at the end.
Provide sources as a list. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

# Set up the retriever and language model (LLM) for the RAG system.
retriever = vectordb.as_retriever(search_kwargs={"k": 10})
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


def format_docs(docs):
    """Formats documents into a single string.

    Args:
        docs: A list of documents to format.

    Returns:
        A string containing the formatted documents.
    """

    return "\n\n".join(doc.page_content for doc in docs)


def rag(prompt):
    """Executes a single RAG chain to generate an answer based on a given prompt.

    Args:
        prompt: The prompt to provide to the RAG system.

    Returns:
        The generated answer as a string.
    """

    # Set up the RAG chain, combining the retriever, prompt formatter, LLM, and output parser.
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    result = rag_chain.invoke(prompt)

    return result


def rag_cl():
    """Interactive command-line interface to continuously run the RAG process.

    Prompts the user for questions, retrieves context, and generates answers until the user quits.
    """
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    while (prompt := input("Enter a prompt (q to quit): ")) != "q":
        result = rag_chain.invoke(prompt)

        print("\n" + result)


if __name__ == "__main__":
    # If this script is executed directly, start the interactive RAG command-line interface.
    rag_cl()
