### Get top papers
import requests
from bs4 import BeautifulSoup
import re


def get_trending_urls() -> list:
    """Pull the trending papers on the front page of paperswithcode.com"""

    # URL to scrape
    url = "https://paperswithcode.com/"

    # Make an HTTP GET request to the URL
    response = requests.get(url)

    # Ensure the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all 'a' tags (hyperlinks) in the document:
        links = soup.find_all("a")

        # regex to match link to research papers
        pattern = r"\/paper\/(?!.*(#code|#tasks)$).*$"
        unique_papers = []

        for link in links:
            href = link.get("href")
            # Check if the href attribute is a string and if it matches the pattern
            if isinstance(href, str) and re.search(pattern, href):
                # If the link is not already in the list, add it
                if href not in unique_papers:
                    unique_papers.append(href)

        # Now, unique_papers contains all unique links that include "/paper/"
    else:
        print(f"Failed to retrieve the webpage: HTTP {response.status_code}")

    paper_urls = []
    for paper in unique_papers:
        paper_urls.append("https://paperswithcode.com" + paper)

    return paper_urls


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


def get_paper_list() -> list:
    paper_urls = get_trending_urls()
    links = [get_arxiv_link(url) for url in paper_urls]
    return links


