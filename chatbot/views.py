import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .nlp.processor import ArabicQARetriever
from .models import UserFatwa
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# Initialize the retriever once when the server starts
if not hasattr(settings, 'retriever'):
    settings.retriever = ArabicQARetriever()
    settings.retriever._load_model()

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن.")
            return redirect('login')
        else:
            messages.error(request, "حدث خطأ أثناء التسجيل. تأكد من صحة البيانات أو اختر اسم مستخدم مختلف.")
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"مرحبًا بك {user.username}!")
            return redirect('chat')
        else:
            messages.error(request, "بيانات تسجيل الدخول غير صحيحة. تأكد من اسم المستخدم وكلمة المرور.")
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})




from django.contrib.auth.decorators import login_required
from .models import UserFatwa

@login_required
def my_fatwas(request):
    fatwas = UserFatwa.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chatbot/my_fatwas.html', {'fatwas': fatwas})


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('chat')




def get_fatwa(request):
    question = request.GET.get('userMessage', '')
    retriever = settings.retriever
    answer = retriever.get_answer(question)

    if request.user.is_authenticated:
        UserFatwa.objects.create(user=request.user, question=question, answer=answer)

    return JsonResponse(answer, safe=False)
def get_random_question(request):
    """Fetch a random question from the dataset"""
    if settings.retriever.qa_pairs:
        random_qa = random.choice(settings.retriever.qa_pairs)
        return JsonResponse({"question": random_qa['title']})
    return JsonResponse({"question": "No random questions available."})

def get_quick_questions(request):
    retriever = settings.retriever
    questions = retriever.get_random_titles(count=5)
    return JsonResponse({"questions": questions})
