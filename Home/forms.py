from django import forms

from django.forms import ModelForm
from .models import User

class UserCreationForm(ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class Join(forms.Form):
    #code = forms.CharField(max_length=100, required=True, label='') 
    access_code = forms.CharField(widget=forms.TextInput(attrs={'size':'30','maxlength':'70'} ), label='')
