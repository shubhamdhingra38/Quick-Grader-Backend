"""
This contains all the ML logic
"""

import pickle
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
from quiz.models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response as APIResponse
from random import shuffle, randint
import json
from collections import defaultdict
from ml import preprocess_text
from scipy import spatial

"""
Machine learning stuff
"""
np.random.seed(42)

PERCENTAGE_CLUSTERS = 0.3

# module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
# model = hub.load(module_url)
# print("module %s loaded" % module_url)
model = hub.load('universal-sentence-encoder-v4')


def embed(input):
    return model([input])


def debug(input):
    print('\n_____________\n')
    print(input)
    print('\n_____________\n')


def get_answers_embedding(answers):
    result = np.zeros((len(answers), 512))
    for i, answer in enumerate(answers):
        result[i] = embed(answer.short_ans)
    return result


def cluster_answers(answers, question_id):
    embeddings = get_answers_embedding(answers)

    # number of clusters according to % of clusters
    l = len(answers)
    n_clusters = max(2, int(PERCENTAGE_CLUSTERS * l))
    debug(f'\tCreating num clusters: {n_clusters}')
    model = KMeans(n_clusters=n_clusters)
    model.fit(embeddings)

    labels = model.labels_

    # get cluster centers
    closest, _ = pairwise_distances_argmin_min(
        model.cluster_centers_, embeddings)

    cluster_centers = []
    map_label_to_centroid = {}
    for i, answer in enumerate(answers):
        if i in closest:
            cluster_centers.append(answer.id)
            map_label_to_centroid[labels[i]] = answer.id

    debug(f'\tCluster centers are: {cluster_centers}, question: {question_id}')

    # mapping from cluster center -> other points in cluster
    map_centroid_to_answer_ids = defaultdict(list)
    for i, answer in enumerate(answers):
        label = labels[i]
        centroid = map_label_to_centroid[label]
        if i not in closest:
            map_centroid_to_answer_ids[centroid].append(answer.id)

    debug(f'\tMap[centroid] -> answers = {map_centroid_to_answer_ids}')

    # save this for later use
    pickle.dump(map_centroid_to_answer_ids, open(
        f'./cached_models/clusters-{question_id}.pkl', 'wb'))

    return cluster_centers


class ClustersGenerate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    # ask to grade these answers
    def post(self, request):
        """
        Get clusters for every question in this quiz.
        """
        quiz_id = request.data['quizID']
        quiz = Quiz.objects.get(author=request.user, id=quiz_id)

        debug(f'Quiz is: {quiz}')

        questions = Question.objects.filter(test=quiz)
        response = {}

        for question in questions:
            debug(f'For question: {question}')
            if question.type == 1:  # short answer
                answers = Answer.objects.filter(question=question)
                debug(f'Answers are: {answers}')
                cluster_centers = cluster_answers(answers, question.id)
                response[question.id] = cluster_centers
            else:
                print('Skipping question of type MCQ')

        return APIResponse(response)


def grade_answer(answer_id, grade):
    answer = Answer.objects.get(pk=answer_id)
    answer.response.total_score -= answer.score
    answer.response.total_score += grade
    answer.response.save()
    answer.score = grade
    answer.save()


class ClusterGrade(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    # after grading the answers (centroids), grade rest of the points
    def post(self, request):
        question_id = request.data['questionID']
        grades = request.data['grades']  # {answer_id: grade}
        question = Question.objects.get(pk=int(question_id))
        answers = Answer.objects.filter(question=question)

        with open(f'./cached_models/clusters-{question_id}.pkl', 'rb') as f:
            map_centroid_to_answer_ids = pickle.load(f)
        for centroid_id in grades:
            grade = grades[centroid_id]
            grade_answer(centroid_id, grade)
            other_answers_in_cluster = map_centroid_to_answer_ids[int(centroid_id)]
            for answer_id in other_answers_in_cluster:
                grade_answer(answer_id, grade)
                

        return APIResponse({"msg": "Ok"})


def cosine_similarity(vec1, vec2):
    return 1 - spatial.distance.cosine(vec1, vec2)
    

def get_similar_answers(answers, threshold):
    answer_texts = [answer.short_ans for answer in answers]
    preprocessed_answers = [' '.join(preprocess_text(answer)) for answer in answer_texts]
    cv = CountVectorizer(stop_words='english')
    vectors = cv.fit_transform(preprocessed_answers).toarray()
    print(vectors)
    most_similar = defaultdict(list)
    for i, v1 in enumerate(vectors):
        similar = []
        for j, v2 in enumerate(vectors):
            if i == j:
                continue
            if cosine_similarity(v1, v2) >= threshold:
                most_similar[answers[i].id].append(answers[j].id)
    return most_similar



class PlagiarismDetectionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def post(self, request):
        quiz_id = int(request.data['quizID'])
        plag_threshold = float(request.data['threshold'])
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = Question.objects.filter(test=quiz)
        similarity_by_responses = defaultdict(lambda: defaultdict(list))
        for question in questions:
            if question.type == 1: #short answer
                answers = Answer.objects.filter(question=question)
                similar_answers_dict = get_similar_answers(answers, plag_threshold)
                print(similar_answers_dict)
                for answer in answers:
                    answer_id = answer.id
                    response_id = answer.response.id
                    for similar_answers_id  in similar_answers_dict[answer_id]:
                        similar_answer = Answer.objects.get(id=similar_answers_id)
                        similarity_by_responses[response_id][similar_answer.response.id].append(question.id)

        return APIResponse(similarity_by_responses)
