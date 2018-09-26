from django import forms

class Join(forms.Form):
    #code = forms.CharField(max_length=100, required=True, label='') 
    access_code = forms.CharField(widget=forms.TextInput(attrs={'size':'30','maxlength':'70'} ), label='')


