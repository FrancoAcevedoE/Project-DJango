from django.urls import path
from . import views

urlpatterns = [
    path("", views.talk_index, name="talk_index"),
]