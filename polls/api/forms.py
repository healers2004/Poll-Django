from django import forms
from ..models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(), widget=forms.RadioSelect, empty_label=None)

    def __init__(self, question_id, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = Choice.objects.filter(question_id=question_id)