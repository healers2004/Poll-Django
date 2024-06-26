from django.urls import path

from . import views

app_name = "polls_api"
urlpatterns = [
    path("polls/", views.QuestionList.as_view(), name="polls_list"),
    path("polls/<int:question_id>/vote/", views.CastVote.as_view(), name="cast_vote"),
    path("questions/html/", views.question_list_view, name="questions_list_html"),  # HTML view
    path("polls/<int:question_id>/vote_form/", views.vote_view, name="vote_form"),  # HTML form view
]

