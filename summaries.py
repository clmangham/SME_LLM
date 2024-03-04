# from get_data import get_paper_info
import json


def get_summaries():
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
