"""polls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""
from django.urls import path

from polls.views import ActivePolls, CreateAnswer, UserAnswersDetail

urlpatterns = [
    path('active', ActivePolls.as_view(), name='active_polls'),
    path('answer', CreateAnswer.as_view(), name='create_answer'),
    path('users/<int:pk>/answers-detail', UserAnswersDetail.as_view(),
         name='user_answers_detail'),
]
