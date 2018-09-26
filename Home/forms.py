from django import forms
from django.forms import ModelForm
from .models import User

class UserCreationForm(ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=False, widget=forms.Textarea())
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


