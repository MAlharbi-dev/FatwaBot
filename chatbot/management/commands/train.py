
from django.core.management.base import BaseCommand
from chatbot.nlp.processor import ArabicQARetriever

class Command(BaseCommand):
    help = 'Train improved Arabic fatwa model'

    def handle(self, *args, **options):
        retriever = ArabicQARetriever()
        retriever.train('chatbot/data/raw_data/Full_BinBaz_Data2.csv')
        self.stdout.write(self.style.SUCCESS(
            f"Trained on {len(retriever.qa_pairs)} QA pairs\n"
            f"Sample question: {retriever.qa_pairs[0]['title'][:30]}..."
        ))