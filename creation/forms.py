from django import forms
from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    choose = (('default', 'Default'), ('hackathon', 'Hackathon'),
              ('School Event', 'School Event'), ('other', 'other'))
    event_type = forms.ChoiceField(
        required=False, widget=forms.Select, choices=choose)
    description = forms.CharField(required=False,widget=forms.Textarea())
    # admin = forms.CharField(max_length=100, required=True)
    title = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Event
        fields = ('title', 'description', 'event_type')


