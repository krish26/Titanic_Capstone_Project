from django.shortcuts import render
from . import forms
from .models import Prediction

def index(request):
    return render(request, 'home.html')

def prediction_form(request):
    if request.method == 'POST':
        form = forms.PredictionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Feature engineering
            family_size = data["sibsp"] + data["parch"] + 1
            is_alone = family_size == 1

            # Placeholders
            survived = False
            survival_probability = 0.0

            prediction = Prediction.objects.create(
                pclass=int(data["pclass"]),
                sex=int(data["sex"]),
                age=data["age"],
                fare=data["fare"],
                embarked=int(data["embarked"]),
                family_size=family_size,
                is_alone=is_alone,
                survived=survived,
                survival_probability=survival_probability
            )

            return render(request, "results.html", {"prediction": prediction})
        else:
            form = forms.PredictionForm()

    return render(request, 'prediction_form.html', {'form': form})

def results(request):
    return render(request, 'results.html')

def history(request):
    return render(request, 'history.html')
