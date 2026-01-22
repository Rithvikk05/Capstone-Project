import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import collections

# Ensure nltk data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('punkt_tab')

def extract_keywords(text, num=5):
    """
    Extracts top keywords from text excluding stopwords.
    """
    if not text:
        return []
        
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    
    keywords = [word for word in tokens if word.isalnum() and word not in stop_words]
    
    counter = collections.Counter(keywords)
    return [word for word, count in counter.most_common(num)]

def generate_study_tips(text):
    """
    Generates study tips based on text content.
    """
    keywords = extract_keywords(text)
    
    if not keywords:
        return ["Review the material again.", "Make sure to take notes."]
    
    tips = [
        f"Focus on defining terms like '{keywords[0]}' and '{keywords[1] if len(keywords)>1 else ''}'.",
        "Create flashcards for the key concepts.",
        "Summarize the main points in your own words.",
        f"Quiz yourself on the relationship between {keywords[0]} and other topics."
    ]
    return tips

if __name__ == "__main__":
    text = "Photosynthesis is the process used by plants to convert light energy into chemical energy."
    print(extract_keywords(text))
    print(generate_study_tips(text))
