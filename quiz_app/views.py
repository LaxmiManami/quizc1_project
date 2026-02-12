from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Quiz

def home(request):
    return render(request, "quiz_app/home.html")

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all().order_by("-created_at")
    return render(request, "quiz_app/quiz_list.html", {"quizzes": quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, "quiz_app/quiz_detail.html", {"quiz": quiz})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == "POST":
        score = 0
        total = questions.count()
        responses = {}
        for q in questions:
            selected = request.POST.get(str(q.id), "")
            responses[q.id] = selected
            if selected == q.correct_answer:
                score += 1
        context = {"quiz": quiz, "score": score, "total": total, "responses": responses, "questions": questions}
        return render(request, "quiz_app/quiz_result.html", context)

    return render(request, "quiz_app/take_quiz.html", {"quiz": quiz, "questions": questions})

@login_required
def review_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    user_answers = request.session.get('user_answers', {})
    context = {'quiz': quiz, 'questions': questions, 'user_answers': user_answers}
    return render(request, "quiz_app/review_quiz.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')