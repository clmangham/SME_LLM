### Get top papers
import requests
from bs4 import BeautifulSoup
import re
from langchain_community.retrievers import ArxivRetriever



def scrape_paper_metadata() -> list:
    """Pull the trending papers on the front page of paperswithcode.com"""

    # URL to scrape
    url = "https://paperswithcode.com/"

    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Ensure the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(response.text, "html.parser")

        # Now you can use Beautiful Soup methods to find data in the soup object
        # For example, to find all 'a' tags (hyperlinks) in the document:
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

        # Now, unique_papers contains all unique links that include "/paper/"
    else:
        print(f"Failed to retrieve the webpage: HTTP {response.status_code}")


    paper_metadata = []
    for paper, title in zip(unique_papers, titles):
        paper_metadata.append({'url': "https://paperswithcode.com" + paper, 'title': title})


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
    retriever = ArxivRetriever(load_max_docs=1)
    paper_metadata = scrape_paper_metadata()

    for data in paper_metadata:
        data['arxiv_link'] = get_arxiv_link(data['url'])

        doc_num = data['arxiv_link'].split('/')[-1][:-4]
        docs = retriever.load(query=doc_num)

        data['published'] = docs[0].metadata['Published']
        data['authors'] = docs[0].metadata['Authors']
        data['summary'] = docs[0].metadata['Summary']

    return paper_metadata

# if 'name' == 'main':

#     paper_metadata = get_paper_info()
#     with open('data/paper_metadata.json', 'w') as file:
#         json.dump(paper_metadata, file, indent=4)

