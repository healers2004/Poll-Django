from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse #, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuestionSerializer
from .models import Choice, Question
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from django.template import loader

# def main(request):
#     template_name = loader.get_template("main.html")
#     return HttpResponse(template_name.render())


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
class CastVote(APIView):
    def post(self, request, question_id):
        choice_id = request.data.get('choice')
        try:
            selected_choice = Choice.objects.get(id=choice_id, question_id=question_id)
        except Choice.DoesNotExist:
            return Response({'error': 'Choice not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        selected_choice.votes += 1
        selected_choice.save()
        
        return Response({'message': 'Vote cast successfully.'}, status=status.HTTP_200_OK)

class QuestionList(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Return only the questions with pub_date less than or equal to now.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
