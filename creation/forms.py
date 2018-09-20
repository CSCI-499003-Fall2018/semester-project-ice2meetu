from django import forms

class NameForm( forms.Form):
    if not hasattr(forms.Form, 'count'):
        count = 0
    else:
        count = forms.Form['count']
    your_name = forms.CharField(label='Your name', max_length=100)
    your_pass = forms.CharField(label='Pass', max_length=100)
    for i in range(count):
        forms.CharField(label='', max_length=100)