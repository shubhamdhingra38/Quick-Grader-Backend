"""
This will contain all the ML logic (might have to go for a separate server for just ML app)
"""

from quiz.models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response as APIResponse
from random import shuffle, randint


N_GROUP_MIN = 2
N_GROUP_MAX = 5


def generate_random_clusters(question):
    answers = Answer.objects.filter(question=question)
    answers = list(answers)
    shuffle(answers)

    grouped_items = []
    i = 0
    while i < len(answers):
        take = min(randint(N_GROUP_MIN, N_GROUP_MAX), len(answers) - i)
        items = [answer.id for answer in answers[i:i+take]]
        grouped_items.append(items)
        i += take

    return grouped_items


class ClusterGrade(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def post(self, request):
        quiz_id = request.data['quizID']
        quiz = Quiz.objects.get(author=request.user, id=quiz_id)

        print('Quiz is', quiz)

        questions = Question.objects.filter(test=quiz)

        for question in questions:
            print(generate_random_clusters(question))

        return APIResponse({"msg": "Ok"})
