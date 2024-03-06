# Trending Research Papers - Summary and AI Chat
##  Project Overview

This project is designed to automate the process of scraping trending research papers from paperswithcode.com, downloading the actual research papers in  the arXiv URLs found in the metadata, and processing this information to generate insights and utility. The paper abstracts are presented on a Streamlit page for easy viewing, while topic modeling techniques are applied to generate relevant keywords for the set of papers Furthermore, the arXiv articles are embedded into a vector database, to facilitate advanced retrieval-augmented generation capabilities.

## Features

- Trending Research Paper Scraping: Automatically scrapes trending research papers from paperswithcode.com.
- Streamlit Summaries: Writes summaries of the papers to a Streamlit page for interactive exploration.
- Keyword Generation: Applies topic modeling to abstracts to generate relevant keywords.
- Q&A on Research: Uses retrieval-augmented generation (RAG) to facilitate question answering regarding the content in each paper.