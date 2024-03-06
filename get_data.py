### Get top papers
import requests
from bs4 import BeautifulSoup
import re
from langchain_community.retrievers import ArxivRetriever
from database import insert_or_update_database
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def scrape_paper_metadata() -> list:
    """Scrape the trending papers' metadata from the front page of paperswithcode.com.

    Returns:
        list: A list of dictionaries, each containing the 'url' and 'title' of a paper.
    """
    # URL to scrape
    url = "https://paperswithcode.com/"

    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Ensure the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(response.text, "html.parser")

        # Use Beautiful Soup methods to find data in the soup object
        # Find all 'a' tags (hyperlinks) in the document:
        a_tags = soup.find_all("a")

        pattern = r"\/paper\/(?!.*(#code|#tasks)$).*$"
        unique_papers = []
        titles = []

        for tag in a_tags:
            href = tag.get("href")
            # Check if the href attribute is a string and if it matches the pattern
            if isinstance(href, str) and re.search(pattern, href) and tag.text.strip():
                # If the link is not already in the list, add it
                if href not in unique_papers:
                    unique_papers.append(href)
                    titles.append(tag.text)

    else:
        print(f"Failed to retrieve the webpage: HTTP {response.status_code}")

    paper_metadata = []
    for paper, title in zip(unique_papers, titles):
        paper_metadata.append(
            {"url": "https://paperswithcode.com" + paper, "title": title}
        )

    return paper_metadata


def get_arxiv_link(url: str) -> str:
    """Get the link to the pdf of the research article

    Args:
        url (str): url of trending paper on paperswith code

    Returns:
        str: the arxiv_link
    """
    pdf_link = None
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(response.text, "html.parser")

        # Define a function that checks if an 'a' tag's 'href' attribute contains the arXiv PDF URL
        def is_arxiv_pdf(tag):
            return (
                tag.name == "a"
                and tag.get("href")
                and "https://arxiv.org/pdf" in tag.get("href")
            )

        # Use the function to filter 'a' tags
        links = soup.find_all(is_arxiv_pdf)

        # Print the 'href' attribute of each link
        for link in links:
            pdf_link = link.get("href")
    else:
        print(f"Failed to retrieve the webpage: HTTP {response.status_code}, {url}")

    return pdf_link


def get_paper_info() -> list:
    # Initialize an ArxivRetriever object to fetch documents from arXiv.
    # The `load_max_docs=1` argument indicates that for each query, only one document should be loaded.
    retriever = ArxivRetriever(load_max_docs=1)

    # Call the scrape_paper_metadata function to obtain the list of trending papers' metadata from paperswithcode.com.
    paper_metadata = scrape_paper_metadata()

    # Iterate over each paper's metadata in the list.
    for data in paper_metadata:
        # Retrieve the arXiv PDF link for the paper and add it to the paper's metadata.
        data["arxiv_link"] = get_arxiv_link(data["url"])

        # Extract the document number from the arXiv link. This assumes the arXiv link format ends with
        # a document number followed by ".pdf" and uses string manipulation to extract this number.
        doc_num = data["arxiv_link"].split("/")[-1][:-4]

        # Use the ArxivRetriever object to load the document from arXiv using the extracted document number.
        # This step fetches the document's metadata from arXiv.
        docs = retriever.load(query=doc_num)

        # Update the paper's metadata with the published date, authors, and summary extracted from the arXiv document's metadata.
        data["published"] = docs[0].metadata["Published"]
        data["authors"] = docs[0].metadata["Authors"]
        data["summary"] = docs[0].metadata["Summary"]

    # The following line would insert or update the obtained metadata into a database.
    # insert_or_update_database(paper_metadata) # Uncomment to use!

    # Specify the filename
    filename = "data/paper_metadata.json"

    # Write the dictionary to a file
    with open(filename, "w") as file:
        json.dump(paper_metadata, file, indent=4)

    print("Metadata saved!")
    # return paper_metadata


def create_vector_database():
    # Specify the filename
    filename = "data/paper_metadata.json"

    # Write the dictionary to a file
    with open(filename, "r") as file:
        paper_metadata = json.load(file)

    # Indexing
    docs = []
    for paper in paper_metadata:
        link = paper["arxiv_link"]
        loader = PyPDFLoader(link)
        doc = loader.load_and_split()
        for idoc in doc:
            idoc.metadata["title"] = paper["title"]
            idoc.metadata["published"] = paper["published"]
            idoc.metadata["authors"] = paper["authors"]
            idoc.metadata["summary"] = paper["summary"]
        docs.extend(doc)

    # Text splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embed and store the texts
    # Supplying a persist dicrectory will store the embeddings on disk
    persist_directory = "data/vectordb"

    embeddings = OpenAIEmbeddings()
    # vectordb = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_direcory)
    Chroma.from_documents(
        documents=splits, embedding=embeddings, persist_directory=persist_directory
    ).persist()
    # vectordb.persist()
    print("Vector database saved!")


if __name__ == "__main__":
    get_paper_info()
    create_vector_database()
