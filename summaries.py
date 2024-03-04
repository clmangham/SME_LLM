# from get_data import get_paper_info
import json

def get_summaries():
    # Specify the filename
    filename = "data/paper_metadata.json"

    # Write the dictionary to a file
    with open(filename, "r") as file:
        paper_metadata = json.load(file)

    i = 0
    for paper in paper_metadata:
        i += 1
        print("\n" + "Paper #" + str(i) + "\n"  + paper['title'])
        print(paper['authors'])
        print(paper['published'])
        print(paper['arxiv_link'])

        print("\n" + 'Summary:')
        print(paper['summary'])


if __name__ == "__main__":
    get_summaries()