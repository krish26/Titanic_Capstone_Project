from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

CHOICES = (
    ('1', 'Male'),
    ('2', 'Female'),
)

class PredictionForm(forms.Form):
    gender = forms.ChoiceField(choices=CHOICES)
