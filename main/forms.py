from django import forms
from .models import Prediction

class PredictionForm(forms.Form):

    pclass = forms.ChoiceField(
        choices=[(1, "1st class"), (2, "2nd class"), (3, "3rd class")],
        label="Passenger class"
    )

    sex = forms.ChoiceField(
        choices=Prediction.SEX_CHOICES,
        label="Sex"
    )

    age = forms.IntegerField(
        min_value=0,
        max_value=100,
        label="Age"
    )

    sibsp = forms.IntegerField(
        min_value=0,
        max_value=20,
        label="Number of siblings / spouses aboard"
    )

    parch = forms.IntegerField(
        min_value=0,
        max_value=20,
        label="Number of parents / children aboard"
    )

    fare = forms.FloatField(
        min_value=0,
        max_value=600,
        label="Fare"
    )

    embarked = forms.ChoiceField(
        choices=Prediction.EMBARKED_CHOICES,
        label="Embarked in port"
    )