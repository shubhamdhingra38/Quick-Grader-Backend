from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('cluster-grade/', views.ClusterGrade.as_view()),

]
