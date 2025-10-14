from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView
from .models import *
import json



class TourList(ListView):
    model = Tour
    ordering = 'tour_name'
    template_name = 'tours_list.html'
    context_object_name = 'tours'
    paginate_by = 3


class TourDetail(DetailView):
    model = Tour
    template_name = 'tour_detail.html'
    context_object_name = 'tour'

class StoryList(ListView):
    model = Story
    ordering = 'created_at'
    context_object_name = 'stories'
    template_name = 'story.html'

class TourDropDownElementsListView(ListView):
    model = TourDropDownElements
    ordering = 'element_created_at'
    context_object_name = 'drop_down_el'
    template_name = 'tours_list.html'

class ProfileDetail(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile.html'

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'phone_number']
    template_name = 'profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class SaveQuizResult(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        quiz_id = data.get("quiz_id")
        score = data.get("score")
        total_questions = data.get("total_questions")

        if not request.user.is_authenticated:
            return JsonResponse({"error": "Необходима авторизация"}, status=403)

        quiz = Quiz.objects.get(id=quiz_id)
        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
        )

        return JsonResponse({"message": "Результат сохранён", "result_id": result.id})


from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Quiz, QuizResult, Question, AnswerOption


# ======= Страница квиза =======
class QuizDetail(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "quiz.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # загружаем вопросы + варианты ответов
        ctx["questions"] = self.object.questions.prefetch_related("answer_options")
        return ctx


# ======= Обработка ответов =======
class QuizSubmit(LoginRequiredMixin, View):
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = quiz.questions.prefetch_related("answer_options")

        score = 0
        total = questions.count()

        for question in questions:
            # имя input в шаблоне = "question_<id>"
            answer_id = request.POST.get(f"question_{question.id}")
            if not answer_id:
                continue  # вопрос пропущен

            try:
                answer = AnswerOption.objects.get(pk=answer_id, question=question)
                if answer.is_correct:
                    score += 1
            except AnswerOption.DoesNotExist:
                pass

        # сохраняем результат
        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total,
        )

        messages.success(
            request,
            f"Ваш результат: {score} из {total}"
        )
        return redirect("quiz_result", pk=result.pk)


# ======= Результат квиза =======
class QuizResultDetail(LoginRequiredMixin, DetailView):
    model = QuizResult
    template_name = "quiz_result.html"
    context_object_name = "result"


@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user_id = data.get("user_id")
        username = data.get("username")

        user, created = User.objects.get_or_create(username=username or f"user_{user_id}")
        profile = user.profile
        profile.first_name = data.get("first_name", "")
        profile.last_name = data.get("last_name", "")
        profile.avatar_url = data.get("avatar_url", "")
        profile.phone_number = data.get("phone_number", "")
        profile.save()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)