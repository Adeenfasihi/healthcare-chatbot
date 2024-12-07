from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from translation import *

# Load dataset
SYMPTOM_DATA = pd.read_csv('data/Symptom2Disease.csv')

# Function to find matching diseases
def find_matching_diseases(user_symptoms, target_langcode, top_n=3):
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
    detected_langcode    = detect_language(user_symptoms)

    # Change target language accordingly
    target_langcode = detected_langcode if target_langcode == "auto" else target_langcode

    # Get language names from the lang_code
    detected_language = decode_langcode(detected_langcode)
    target_language = decode_langcode(target_langcode)

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

    # Create a dictionary of out of the matches
    top_matches_dict = top_matches.to_dict(orient='records')

    # Concatenate the top_n results
    response_string = "\n\n".join([f"{match['label']}: {match['text']}" for match in top_matches_dict])
    
    # Translate response to the target language
    response_in_target_language = translate_sentence(response_string, target_langcode)
        
    return {
        "tokens": tokens,
        "top_matches_dict": top_matches_dict,
        "symptoms_in_english": symptoms_in_english,
        "detected_language": detected_language,
        "target_language": target_language,
        "response_in_target_language": response_in_target_language,
    }