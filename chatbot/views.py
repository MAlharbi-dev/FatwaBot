from django.shortcuts import render
from django.http import JsonResponse
from .nlp.processor import ArabicQARetriever

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def get_fatwa(request):
    question = request.GET.get('userMessage', '')
    retriever = ArabicQARetriever()
    answer = retriever.get_answer(question)
    return JsonResponse(answer, safe=False)  # Return plain text