from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from .serializers import QuestionSerializer
from ..models import Question, Choice
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .forms import VoteForm

class CastVote(APIView):
    permission_classes = [AllowAny]  # Allow any user to cast a vote
    
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

def question_list_view(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    return render(request, 'polls/question_list.html', {'questions': questions})

def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = VoteForm(question_id, request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            choice.votes += 1
            choice.save()
            return redirect('polls:results', pk=question.id)
    else:
        form = VoteForm(question_id)

    return render(request, 'polls/vote.html', {'question': question, 'form': form})