# Trending Research Papers - Summary and AI Chat
##  Project Overview

This project is designed to automate the process of scraping trending research papers from paperswithcode.com, downloading the actual research papers in  the arXiv URLs found in the metadata, and processing this information to generate insights and utility. The paper abstracts are presented on a Streamlit page for easy viewing, while topic modeling techniques are applied to generate relevant keywords for the set of papers Furthermore, the arXiv articles are embedded into a vector database, to facilitate advanced retrieval-augmented generation capabilities.

## Features

- Trending Research Paper Scraping: Automatically scrapes trending research papers from paperswithcode.com.
- PDF Retrieval: Downloads research papers in PDF format from arXiv.
- Streamlit Summaries: Writes summaries of the papers to a Streamlit page for interactive exploration.
- Keyword Generation: Applies topic modeling to abstracts to generate relevant keywords.
- Vector Database Embedding: Embeds articles into ChromaDB for enhanced retrieval capabilities.
- Q&A on Research Papers: Leverages retrieval-augmented generation (RAG) for question answering based on the paper content.

## Installation
```
git clone https://github.com/clmangham/SME_LMM.git
cd SME_LLM
pip install -r requirements.txt
```

## Configuration

AN API key should be stored in a .env file in the root of the directory like so:
```
OPENAI_API_KEY="API KEY HERE"
```

## Usage
```
# Pull and save data to /data
python get_data.py

# Run streamlit app
streamlit run main.py
```

## Potential Improvements
- Pull new data automatically on a regular basis (get_data.py)
- Improve topic modeling to provide topics keywords for each abstract specifically (topic_modeling.py)
- Experiment with different topic models
- Add chat history to rag to create chatbot that can answer follow-up questions (rag.py)
    - https://python.langchain.com/docs/use_cases/question_answering/chat_history
- Experiment with different LLM models and how to best evaluate their performance, including prompt engineering, question generation for retrieval evaluation, and metrics such as LLM output relevance and latency:
    - https://mlflow.org/docs/latest/llms/index.html
    - https://mlflow.org/docs/latest/llms/rag/notebooks/question-generation-retrieval-evaluation.html
    - https://mlflow.org/docs/latest/llms/rag/notebooks/retriever-evaluation-tutorial.html
    - https://mlflow.org/docs/latest/llms/llm-evaluate/index.html
    - https://mlflow.org/docs/latest/llms/prompt-engineering/index.html

- Containerize for consistent development and deployment