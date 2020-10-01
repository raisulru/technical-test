#-*- coding: utf-8 -*-
from django.urls import path, include
from mailer.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
]
