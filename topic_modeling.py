import json
import pickle
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
import openai
from bertopic.representation import OpenAI, KeyBERTInspired
from bertopic import BERTopic

def topic_modeling():
    filename = "data/paper_metadata.json"

    # Write the dictionary to a file
    with open(filename, "r") as file:
        paper_metadata = json.load(file)


    abstracts = []
    titles = []
    for paper in paper_metadata:
        abstracts.append(paper['summary'])
        titles.append(paper['title'])

    # Pre-calculate embeddings
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(abstracts, show_progress_bar=True)


    # Reduce stochastic behavior with UMAP
    umap_model = UMAP(n_neighbors=2, n_components=1, min_dist=0.0, metric='cosine', random_state=42)

    # Control Number of Topics with HDBSCAN
    hdbscan_model = HDBSCAN(min_cluster_size=2, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

    # Improve Default Representaiton with CountVectorizor
    vectorizer_model = CountVectorizer(stop_words="english", min_df=1, ngram_range=(1, 2))


    # KeyBERT
    keybert_model = KeyBERTInspired()


    # Open AI Represenation - GPT-3.5
    prompt = """
    I have a topic that contains the following documents:
    [DOCUMENTS]
    The topic is described by the following keywords: [KEYWORDS]

    Based on the information above, extract a short but highly descriptive topic label of at most 5 words. Make sure it is in the following format:
    topic: <topic label>
    """

    # REMOVE KEYS
    client = openai.OpenAI(api_key="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")
    openai_model = OpenAI(client, model="gpt-3.5-turbo", exponential_backoff=True, chat=True, prompt=prompt)

    # All representation models
    representation_model = {
        "KeyBERT": keybert_model,
        # "OpenAI": openai_model
    }

    # Fit model
    topic_model = BERTopic(

    # Pipeline models
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    representation_model=representation_model,

    # Hyperparameters
    top_n_words=10,
    verbose=True
    )

    topics, probs = topic_model.fit_transform(abstracts, embeddings)

    # # Get ChatGPT's labels
    # chatgpt_topic_labels = {topic: " | ".join(list(zip(*values))[0]) for topic, values in topic_model.topic_aspects_["OpenAI"].items()}
    # chatgpt_topic_labels[-1] = "Outlier Topic"
    # topic_model.set_topic_labels(chatgpt_topic_labels)

    # for i, paper in enumerate(paper_metadata):
    #     topic_id = topics[i]
    #     topic_list = topic_model.get_topic_info()['KeyBERT'][topic_id]

    #     paper['topic_id'] = topic_id
    #     paper['topics'] = topic_list

    # with open(filename, 'w') as file:
    #     json.dump(paper_metadata, file, indent=4)

    # print("Metadata updated with topics!")


    # Count and describe topics:
    n_topic_list = len(topic_model.get_topic_info()['KeyBERT'])

    n_topic_list = len(topic_model.get_topic_info()['KeyBERT'])

    topic_lists = []
    for i in range(n_topic_list):
        topic_lists.append(topic_model.get_topic_info()['KeyBERT'][i])


    # Structure to save
    topics_dict = {}
    # topics_dict['topic_model'] = topic_model
    topics_dict['topics'] = topics
    topics_dict['probs'] = probs
    topics_dict['n_topic_list'] = n_topic_list
    topics_dict['topic_lists'] = topic_lists

    # Save for easy loading
    filename = "data/topic_data.pkl"

    with open(filename, 'wb') as file:
        pickle.dump(topics_dict, file)

    print("Topics data saved!")

    return None


if __name__ == "__main__":
    topic_modeling()