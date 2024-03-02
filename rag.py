import json
from langchain_community.document_loaders import PyPDFLoader






# docs = []
# for link, title in zip(links,titles):
#     loader = PyPDFLoader(link)
#     doc = loader.load_and_split()
#     for i in range(len(doc)):
#         doc[i].metadata['title'] = title
#     docs.extend(doc)