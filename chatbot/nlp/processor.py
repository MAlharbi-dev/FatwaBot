import os
import pandas as pd
import pickle
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
        
    def load_model(self):
        """Safe model loading with error handling"""
        try:
            with open(self.model_path, 'rb') as f:
                self.vectorizer, self.model, self.qa_pairs = pickle.load(f)
            return True
        except Exception as e:
            print(f"Model loading failed: {str(e)}")
            return False

    def get_answer(self, question):
        if not self.model and not self.load_model():
            return "حدث خطأ في النظام"
            
        try:
            query_vec = self.vectorizer.transform([question])
            distances, indices = self.model.kneighbors(query_vec)
            return self.qa_pairs[indices[0][0]]['answer']
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return "لا يمكن معالجة السؤال حالياً"