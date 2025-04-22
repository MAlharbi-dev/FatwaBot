from django.core.management.base import BaseCommand
from chatbot.nlp.processor import ArabicQARetriever
import pandas as pd

class Command(BaseCommand):
    help = 'Train improved Arabic fatwa model using multiple datasets'

    def handle(self, *args, **options):
        # Load both datasets
        bin_baz_df = pd.read_csv('chatbot/data/raw_data/Full_BinBaz_Data2.csv')
        othaimin_df = pd.read_csv('chatbot/data/raw_data/Al_Shaikh_Mohammad_Ibn_Othaimin_after_removing_frequent_words.csv')

        # Combine them into one dataset
        combined_df = pd.concat([bin_baz_df, othaimin_df], ignore_index=True)

        # Save combined dataset (optional: for traceability or caching)
        combined_df.to_csv('chatbot/data/raw_data/combined_dataset.csv', index=False)

        # Train retriever on combined dataset
        retriever = ArabicQARetriever()
        retriever.train('chatbot/data/raw_data/combined_dataset.csv')

        self.stdout.write(self.style.SUCCESS(
            f"Trained on {len(retriever.qa_pairs)} QA pairs\n"
            f"Sample question: {retriever.qa_pairs[0]['title'][:30]}..."
        ))
