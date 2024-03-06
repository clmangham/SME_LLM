import json
import pickle
import os
import dotenv
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
import openai
from bertopic.representation import OpenAI, KeyBERTInspired
from bertopic import BERTopic


def topic_modeling():
    """
    Performs topic modeling on a dataset of paper summaries and titles loaded from a JSON file.
    This process involves several steps including loading and preprocessing data, generating
    text embeddings, reducing dimensionality, clustering to identify topics, and finally,
    saving the processed topic data for future use.

    The function uses a pre-trained SentenceTransformer model to generate embeddings for the abstracts,
    UMAP for dimensionality reduction, HDBSCAN for clustering, CountVectorizer for improving topic representation,
    and KeyBERTInspired model for keyword extraction-based topic labeling. Optionally, an OpenAI GPT-3.5 model can
    be used for generating topic labels based on the documents and keywords.

    Environmental Variables:
    - OPENAI_API_KEY: The API key for OpenAI, loaded from a .env file.

    Outputs:
    - Saves the topics, probabilities, number of topics, and detailed topic information in a pickle file
      named 'topic_data.pkl' within the 'data' directory.

    Returns:
    - None
    """
    # Load environment variables from .env file
    dotenv.load_dotenv()

    # Load paper metadata from a JSON file.
    filename = "data/paper_metadata.json"
    with open(filename, "r") as file:
        paper_metadata = json.load(file)

    # Extract summaries and titles from the metadata.
    abstracts = []
    titles = []
    for paper in paper_metadata:
        abstracts.append(paper["summary"])
        titles.append(paper["title"])

    # Generate embeddings for the abstracts using a pre-trained SentenceTransformer model.
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(abstracts, show_progress_bar=True)

    # Use UMAP to reduce the dimensionality of embeddings, aiming to reduce stochastic behavior.
    umap_model = UMAP(
        n_neighbors=2, n_components=1, min_dist=0.0, metric="cosine", random_state=42
    )

    # Apply HDBSCAN to identify clusters within the reduced-dimensional embeddings, controlling the number of topics.
    hdbscan_model = HDBSCAN(
        min_cluster_size=2,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )

    # Use CountVectorizer to improve topic representation by extracting keyword features from the texts.
    vectorizer_model = CountVectorizer(
        stop_words="english", min_df=1, ngram_range=(1, 2)
    )

    # Initialize a KeyBERTInspired model for keyword extraction-based topic labeling.
    keybert_model = KeyBERTInspired()

    # Set up an OpenAI GPT-3.5 model to generate topic labels based on the documents and keywords, providing a custom prompt template.
    prompt = """
    I have a topic that contains the following documents:
    [DOCUMENTS]
    The topic is described by the following keywords: [KEYWORDS]

    Based on the information above, extract a short but highly descriptive topic label of at most 5 words. Make sure it is in the following format:
    topic: <topic label>
    """

    # Access the API key
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)
    openai_model = OpenAI(
        client,
        model="gpt-3.5-turbo",
        exponential_backoff=True,
        chat=True,
        prompt=prompt,
    )

    # Combine the KeyBERT and OpenAI models for topic representation.
    representation_model = {
        "KeyBERT": keybert_model,
        # "OpenAI": openai_model # Uncomment to use
    }

    # Initialize and fit the BERTopic model with the specified models and hyperparameters.
    topic_model = BERTopic(
        # Pipeline models
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        representation_model=representation_model,
        # Hyperparameters
        top_n_words=10,
        verbose=True,
    )

    # Transform the abstracts into topics and probabilities.
    topics, probs = topic_model.fit_transform(abstracts, embeddings)

    # # Use ChatGPT's labels
    # chatgpt_topic_labels = {topic: " | ".join(list(zip(*values))[0]) for topic, values in topic_model.topic_aspects_["OpenAI"].items()}
    # chatgpt_topic_labels[-1] = "Outlier Topic"
    # topic_model.set_topic_labels(chatgpt_topic_labels)

    # # Update metadata with topics
    # for i, paper in enumerate(paper_metadata):
    #     topic_id = topics[i]
    #     topic_list = topic_model.get_topic_info()['KeyBERT'][topic_id]

    #     paper['topic_id'] = topic_id
    #     paper['topics'] = topic_list

    # with open(filename, 'w') as file:
    #     json.dump(paper_metadata, file, indent=4)

    # print("Metadata updated with topics!")

    # Extract and count the number of topics identified.
    n_topic_list = len(topic_model.get_topic_info()["KeyBERT"])

    # Collect detailed information about each topic.
    topic_lists = []
    for i in range(n_topic_list):
        topic_lists.append(topic_model.get_topic_info()["KeyBERT"][i])

    # Prepare a dictionary to save topic data.
    topics_dict = {
        "topics": topics,
        "probs": probs,
        "n_topic_list": n_topic_list,
        "topic_lists": topic_lists,
    }

    # Save the topic data to a pickle file for easy loading.
    filename = "data/topic_data.pkl"

    with open(filename, "wb") as file:
        pickle.dump(topics_dict, file)

    print("Topics data saved!")

    return None


if __name__ == "__main__":
    topic_modeling()
