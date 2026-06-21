from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("session/<str:session_id>/delete/", views.delete_session, name="delete_session"),
]
