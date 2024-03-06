# from get_data import get_paper_info
import json


def get_summaries():
    """
    Loads paper metadata from a JSON file and extracts summaries for each paper.

    This function reads the 'paper_metadata.json' file to retrieve metadata for a list of papers.
    It then formats this metadata to create a summary string for each paper, which includes the
    paper's title, authors, publication date, link to the paper, and the summary text itself.
    These summary strings are compiled into a list, with each element representing a single paper's summary.

    Returns:
        list of str: A list containing formatted summary strings for each paper. Each summary string
        includes the paper's title, authors, publication date, a link to the paper, and the summary text.
    """
    # Specify the filename
    filename = "data/paper_metadata.json"

    # Write the dictionary to a file
    with open(filename, "r") as file:
        paper_metadata = json.load(file)

    # List for paper summaries
    paper_summaries = []

    i = 0
    for paper in paper_metadata:
        i += 1
        # Concatenate all the required information into a single string for each paper
        summary_string = (
            f"\n#{i}\n{paper['title']}\n"
            f"\nAuthors: {paper['authors']}\n"
            f"\nPublished: {paper['published']}\n"
            f"\nLink to paper: {paper['arxiv_link']}\n"
            "\nSummary:\n"
            f"\n{paper['summary']}"
        )
        paper_summaries.append(summary_string)

    return paper_summaries


if __name__ == "__main__":
    summaries = get_summaries()
    for summary in summaries:
        print(summary)
