from get_data import get_paper_info

def get_summaries():
    meta = get_paper_info()
    for paper in meta:
        print("\n" + paper['title'])
        print(paper['authors'])
        print(paper['published'])
        print(paper['arxiv_link'])

        print("\n" + 'Summary:')
        print(paper['summary'])


if __name__ == "__main__":
    get_summaries()