from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('cluster-grade/', views.ClusterGrade.as_view()),
    path('clusters-generate/', views.ClustersGenerate.as_view()),
    path('plagiarism-detection/', views.PlagiarismDetectionView.as_view()),
    path('set-plagiarism/', views.PlagiarismChangeView.as_view()),
]
