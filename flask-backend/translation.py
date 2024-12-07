import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from googletrans import Translator
from langdetect import detect
import langcodes

# Initialize NLTK
nltk.download('punkt')          # For tokenization
nltk.download('stopwords')      # For stopwords
nltk.download('wordnet')        # For lemmatization

STOP_WORDS = set(stopwords.words('english'))
LEMMATIZER = WordNetLemmatizer()

def tokenize(text):
    words = word_tokenize(text)
    filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
    lemmatized_words = [LEMMATIZER.lemmatize(t) for t in filtered_words]
    
    return lemmatized_words

def translate_sentence(text, target_lang='en'):
    try:
        return Translator().translate(text, src='auto', dest=target_lang).text
    except Exception as e:
        return f"There was an error in translation: {str(e)}"

def detect_language(text):
    lang_code = detect(text)    
    return lang_code

def decode_langcode(lang_code):
    language = langcodes.get(lang_code).language_name()
    
    return {"language": language} if language else {"language": "Unknown"}