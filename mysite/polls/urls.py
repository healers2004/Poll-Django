from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path("home/", views.main, name="home"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("api/v1/polls/", views.QuestionList.as_view(), name="polls_list"),
    path("create/", views.CreateQuestion.as_view(), name="create_question"),
]