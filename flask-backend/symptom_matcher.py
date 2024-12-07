from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from translation import *

# Load dataset
SYMPTOM_DATA = pd.read_csv('data/Symptom2Disease.csv')

# Function to find matching diseases
def find_matching_diseases(user_symptoms, target_language, top_n=3):
    """
    Match user symptoms to the dataset using TF-IDF vectorization and cosine similarity.
    Args:
    - user_symptoms (str): The symptoms described by the user.
    - data (DataFrame): The dataset containing symptoms and diseases.
    - top_n (int): Number of top matches to return.

    Returns:
    - matches (list): List of top matches with diseases and similarity scores.
    """

    tokens               = tokenize(user_symptoms)
    symptoms_in_english  = translate_sentence(user_symptoms)
    detected_language    = detect_language(user_symptoms)

    # Combine user symptoms with the dataset for vectorization
    combined_texts = [symptoms_in_english] + SYMPTOM_DATA['text'].tolist()

    # Vectorize using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(combined_texts)

    # Compute cosine similarity between user input and all dataset entries
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Add similarity scores to the dataset
    SYMPTOM_DATA['similarity'] = similarity_scores

    # Sort by similarity and return top matches
    top_matches = SYMPTOM_DATA.nlargest(top_n, 'similarity')[['label', 'text', 'similarity']]

    top_matches_dict = top_matches.to_dict(orient='records')

    # Translate response back to user's language
    response_in_user_language = "\n\n".join([f"{match['label']}: {match['text']}" for match in top_matches_dict])

    response_in_target_language = \
        translate_sentence(response_in_user_language, target_language) \
        if detected_language != target_language else response_in_user_language
    
    return {
        "tokens": tokens,
        "top_matches_dict": top_matches_dict,
        "symptoms_in_english": symptoms_in_english,
        "detected_language": detected_language,
        "response_in_target_language": response_in_target_language,
    }