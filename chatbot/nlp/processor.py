import os
import re
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ArabicQARetriever:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), '../data/model.pkl')
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.qa_pairs = []
        self.embeddings = None

    def _clean_arabic(self, text):
        text = re.sub(r'[^\u0600-\u06FF\s]', '', str(text))
        return re.sub(r'\s+', ' ', text).strip()

    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.qa_pairs, self.embeddings = pickle.load(f)
            return True
        except Exception as e:
            print(f"Model load error: {str(e)}")
            return False

    def train(self, csv_path):
        df = pd.read_csv(csv_path, encoding='utf-8-sig')

        self.qa_pairs = [{
            'title': self._clean_arabic(row['titles']),
            'answer': row['answers']
        } for _, row in df.iterrows() if pd.notna(row['titles'])]

        titles = [q['title'] for q in self.qa_pairs]
        self.embeddings = self.model.encode(titles, show_progress_bar=True)

        # Save model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump((self.qa_pairs, self.embeddings), f)

    def get_answer(self, question):
        if self.embeddings is None and not self.load_model():
            return "حدث خطأ في تحميل النموذج"

        try:
            clean_q = self._clean_arabic(question)
            query_vec = self.model.encode([clean_q])
            similarities = cosine_similarity(query_vec, self.embeddings)[0]
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]

            if best_score > 0.6:  # Adjust the threshold as needed
                return self.qa_pairs[best_idx]['answer']
            return "لم أجد فتوى مطابقة. حاول استخدام كلمات أخرى من العنوان"
        except Exception as e:
            print(f"Error: {str(e)}")
            return "عذراً، حدث خطأ أثناء البحث"
