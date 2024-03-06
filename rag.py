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

# # Specify the filename
# filename = "data/paper_metadata.json"

# # Write the dictionary to a file
# with open(filename, "r") as file:
#     paper_metadata = json.load(file)

# # Indexing
# docs = []
# for paper in paper_metadata:
#     link = paper["arxiv_link"]
#     loader = PyPDFLoader(link)
#     doc = loader.load_and_split()
#     for idoc in doc:
#         idoc.metadata["title"] = paper["title"]
#         idoc.metadata["published"] = paper["published"]
#         idoc.metadata["authors"] = paper["authors"]
#         idoc.metadata["summary"] = paper["summary"]
#     docs.extend(doc)

# # Text splitting
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)

# #Embed and store the texts
# # Supplying a persist dicrectory will store the embeddings on disk
# persist_direcory = 'data/vectordb'

# embeddings = OpenAIEmbeddings()
# vectordb = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_direcory)
# vectordb.persist()

## Load vectorized data
persist_directory = "data/vectordb"
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# Prompt Template
template = """You are an assistant for question-answering tasks regarding trending research (the context). Use the following pieces of context to answer the question at the end.
Provide sources as a list. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectordb.as_retriever(search_kwargs={"k": 10})
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def rag(prompt):
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    # while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    #     result = rag_chain.invoke(prompt)

    #     print("\n" + result)

    result = rag_chain.invoke(prompt)

    return result


def rag_cl():
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
    rag_cl()
