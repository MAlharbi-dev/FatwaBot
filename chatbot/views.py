import random
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .nlp.processor import ArabicQARetriever

# Initialize the retriever once when the server starts
if not hasattr(settings, 'retriever'):
    settings.retriever = ArabicQARetriever()
    settings.retriever.load_model()

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def get_fatwa(request):
    question = request.GET.get('userMessage', '')
    retriever = settings.retriever  # Retrieve the cached retriever
    answer = retriever.get_answer(question)
    return JsonResponse(answer, safe=False)  # Return plain text

def get_random_question(request):
    """Fetch a random question from the dataset"""
    if settings.retriever.qa_pairs:
        random_qa = random.choice(settings.retriever.qa_pairs)
        return JsonResponse({"question": random_qa['title']})
    return JsonResponse({"question": "No random questions available."})