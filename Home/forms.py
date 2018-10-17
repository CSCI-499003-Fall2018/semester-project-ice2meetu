from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class Join(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Your Name')
    access_code = forms.CharField(widget=forms.TextInput(attrs={'size':'30','maxlength':'70'} ), label='')
