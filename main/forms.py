from django import forms

class PredictionForm(forms.Form):

    pclass = forms.ChoiceField(
        choices=[(1, "1st class"), (2, "2nd class"), (3, "3rd class")],
        label="Passenger class"
    )

    sex = forms.ChoiceField(
        choices=[(0, "Male"), (1, "Female")],
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
        max_value=1000,  # TODO: choose a better max_value based on data
        label="Fare"
    )

    embarked = forms.ChoiceField(
        choices=[(1, "Cherbourg"), (2, "Queenstown"), (3, "Southampton")],
        label="Embarked in port"
    )