import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, f1_score
import pickle
import os

class QuizGenerator:
    def __init__(self):
        self.difficulty_model = None
        self.topic_model = None
        self.vectorizer = None
        self.tfidf = None
        self.data_clustered = None

    def _create_difficulty_labels(self, texts):
        # Heuristic: Shorter texts are 'Easy', Longer are 'Medium'
        # Split by median length
        lengths = [len(t.split()) for t in texts]
        median_len = np.median(lengths)
        labels = ['Easy' if l < median_len else 'Medium' for l in lengths]
        return labels

    def train(self, df):
        print("Training Quiz Generator Models...")
        texts = df['cleaned_text'].tolist()
        
        # 1. Train Difficulty Classifier (Logistic Regression)
        labels = self._create_difficulty_labels(texts)
        
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(texts)
        y = labels
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.difficulty_model = LogisticRegression()
        self.difficulty_model.fit(X_train, y_train)
        
        preds = self.difficulty_model.predict(X_test)
        print(f"Difficulty Classifier Accuracy: {accuracy_score(y_test, preds):.2f}")
        print(f"Difficulty Classifier F1 Score: {f1_score(y_test, preds, average='weighted'):.2f}")

        # 2. Train Topic Clusterer (K-Means)
        # We use simple subject-based logic mainly, but K-Means helps find related questions
        self.tfidf = TfidfVectorizer(stop_words='english')
        X_tfidf = self.tfidf.fit_transform(texts)
        
        # Determine K based on unique topics or just set to 5
        k = 5
        self.topic_model = KMeans(n_clusters=k, random_state=42)
        clusters = self.topic_model.fit_predict(X_tfidf)
        
        # Store clusters in dataframe for retrieval
        self.data_clustered = df.copy()
        self.data_clustered['cluster'] = clusters
        
        # Predict difficulty for all rows to use in generation
        all_X = self.vectorizer.transform(texts)
        self.data_clustered['difficulty'] = self.difficulty_model.predict(all_X)
        
        print("Training complete.")

    def generate_quiz(self, subject, difficulty="Easy", num_questions=5):
        if self.data_clustered is None:
            return []
        
        # Filter by subject OR topic (broad search)
        # Search in both 'subject' and 'topic' columns
        mask = (
            self.data_clustered['subject'].str.contains(subject, case=False, na=False) |
            self.data_clustered['topic'].str.contains(subject, case=False, na=False)
        )
        subset = self.data_clustered[mask]
        
        if subset.empty:
            subset = self.data_clustered # Fallback
            
        # Filter by difficulty
        filtered = subset[subset['difficulty'] == difficulty]
        
        if filtered.empty:
            filtered = subset # Fallback if no specific difficulty matches

        # Ensure unique questions by text content logic
        filtered = filtered.drop_duplicates(subset=['text'])
            
        # Sample questions
        n = min(len(filtered), num_questions)
        if n == 0:
            return []
            
        selected = filtered.sample(n)
        
        # Get all unique topics for distractors
        all_topics = self.data_clustered['topic'].unique()
        
        quiz = []
        for _, row in selected.iterrows():
            # Create a more natural question snippet
            snippet = row['text']
            if len(snippet) > 60:
                snippet = snippet[:60] + "..."
                
            question = f"What is the main concept discussed in: '{snippet}'?"
            
            correct_topic = row['topic']
            
            # Smart Distractors: Try to pick from same subject first
            # Filter data for potential distractors from the same subject
            distractor_pool = self.data_clustered[self.data_clustered['subject'] == row['subject']]['topic'].unique()
            
            # Remove correct answer from pool
            distractor_pool = [t for t in distractor_pool if t != correct_topic]
            
            # If not enough, expand to all topics
            if len(distractor_pool) < 3:
                distractor_pool = [t for t in all_topics if t != correct_topic]
                
            # Sample 3 distractors
            if len(distractor_pool) >= 3:
                distractors = list(np.random.choice(distractor_pool, 3, replace=False))
            else:
                 # Fallback if somehow still not enough (very small dataset)
                 distractors = ["Topic A", "Topic B", "Topic C"]
            
            options = distractors + [correct_topic]
            np.random.shuffle(options)
            
            quiz.append({
                "question": question,
                "options": options,
                "correct": correct_topic,
                "context": row['text']
            })
            
        return quiz
    
    def suggest_resources(self, subject):
        # Resource Suggestion System
        # Simple mapping or based on clusters
        resources = {
            "Science": ["https://www.khanacademy.org/science", "https://en.wikipedia.org/wiki/Science"],
            "Math": ["https://www.khanacademy.org/math", "https://wolframalpha.com"],
            "History": ["https://www.history.com", "https://en.wikipedia.org/wiki/History"],
            "Computer Science": ["https://www.w3schools.com", "https://stackoverflow.com"]
        }
        return resources.get(subject, ["https://www.google.com/search?q=" + subject])

    def save_model(self, path="models/quiz_generator.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
            
    @staticmethod
    def load_model(path="models/quiz_generator.pkl"):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return QuizGenerator()

if __name__ == "__main__":
    # Test run
    from data_utils import load_data
    df = load_data("data/dataset.csv")
    if df is not None:
        qg = QuizGenerator()
        qg.train(df)
        qg.save_model()
        print(qg.generate_quiz("Science", "Easy"))
