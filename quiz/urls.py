from django.contrib import admin
from django.urls import path
from .views import (QuizListView, QuestionListView, ChoiceView, AnswerView,
                    ResponseView, CreatedTestsView, Grade, QuizInstanceView,
                    get_report, lock_unlock_quiz, set_plagiarism, ResponseLogsView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'quiz', QuizListView)
router.register(r'question', QuestionListView)
router.register(r'choice', ChoiceView)
router.register(r'answer', AnswerView)
router.register(r'response', ResponseView)

urlpatterns = router.urls
urlpatterns += [
    path('quiz/instance/<str:code>/', QuizInstanceView.as_view(), name="quiz-instance"),
    path('mytests/', CreatedTestsView.as_view()),
    path('grade/', Grade.as_view()),
    path('report/<str:code>/', get_report),
    path('quiz/lock/<str:code>/', lock_unlock_quiz),
    path('quiz/plagiarize/<int:response_id>/', set_plagiarism),
    path('logs/', ResponseLogsView.as_view()),
]
