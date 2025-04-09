import os
import re
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class ArabicQARetriever:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), '../data/model.pkl')
        self.vectorizer = TfidfVectorizer(
            analyzer='word',
            token_pattern=r'\b\w+\b',
            ngram_range=(1, 2)
        )
        self.model = None
        self.qa_pairs = []
        
    def _clean_arabic(self, text):
        """Enhanced Arabic text cleaning"""
        text = re.sub(r'[^\u0600-\u06FF\s]', '', str(text))  # Arabic-only
        return re.sub(r'\s+', ' ', text).strip()

    def load_model(self):
        """Load pre-trained title-answer pairs"""
        try:
            with open(self.model_path, 'rb') as f:
                self.vectorizer, self.model, self.qa_pairs = pickle.load(f)
            return True
        except Exception as e:
            print(f"Model load error: {str(e)}")
            return False

    def train(self, csv_path):
        """Train on title-answer pairs"""
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        # Use title as key, answer as value
        self.qa_pairs = [{
            'title': self._clean_arabic(row['titles']),
            'answer': row['answers']
        } for _, row in df.iterrows() if pd.notna(row['titles'])]
        
        # Train on titles
        titles = [q['title'] for q in self.qa_pairs]
        X = self.vectorizer.fit_transform(titles)
        self.model = NearestNeighbors(n_neighbors=1, metric='cosine').fit(X)
        
        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.vectorizer, self.model, self.qa_pairs), f)

    def get_answer(self, question):
        """Retrieve answer by matching question to nearest title"""
        if not self.model and not self.load_model():
            return "حدث خطأ في تحميل النموذج"
            
        try:
            clean_q = self._clean_arabic(question)
            query_vec = self.vectorizer.transform([clean_q])
            distances, indices = self.model.kneighbors(query_vec)
            
            if distances[0][0] < 0.4:  # Similarity threshold
                return self.qa_pairs[indices[0][0]]['answer']
            return "لم أجد فتوى مطابقة. حاول استخدام كلمات أخرى من العنوان"
        except Exception as e:
            print(f"Error: {str(e)}")
            return "عذراً، حدث خطأ أثناء البحث"