
import os
import re
import pickle
import unicodedata
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from openai import OpenAI

client = OpenAI(api_key="")

class ArabicQARetriever:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.qa_pairs = []
        self.embeddings = None
        self._load_model()

    def _clean_arabic(self, text):
        text = unicodedata.normalize('NFD', str(text))
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        text = re.sub(r'[^؀-ۿ\s]', '', text)
        return re.sub(r'\s+', ' ', text).strip()

    def _load_model(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), '../data/model.pkl'), 'rb') as f:
                self.qa_pairs, self.embeddings = pickle.load(f)
        except Exception as e:
            print(f"❌ فشل تحميل النموذج: {e}")

    def _ask_gpt(self, question, top_fatwas):
        prompt = (
            "أنت مساعد شرعي تجيب على الأسئلة بناءً فقط على هذه الفتاوى:\n"
            + "\n".join(f"- {x}" for x in top_fatwas)
            + f"\n\nالسؤال: {question}"
        )

        try:
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "أجب بدقة فقط بناءً على الفتاوى التالية، ولا تضف أي فتوى من عندك."},
                    {"role": "user", "content": prompt}
                ]
            )
            return res.choices[0].message.content
        except Exception as e:
            return f"⚠️ GPT Error: {str(e)}"

    def get_answer(self, question):
        try:
            clean_q = self._clean_arabic(question)
            q_vec = self.model.encode([clean_q])
            q_vec = q_vec / np.linalg.norm(q_vec, axis=1, keepdims=True)

            sims = cosine_similarity(q_vec, self.embeddings)[0]
            top = [self.qa_pairs[i]['answer'] for i in sims.argsort()[-10:][::-1]]

            return self._ask_gpt(question, top)
        except Exception as e:
            return "❌ حدث خطأ أثناء معالجة السؤال."
