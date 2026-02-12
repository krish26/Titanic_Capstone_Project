from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Prediction
from ML.inference import predict_survival


def index(request):
    return render(request, 'home.html')

def prediction_form(request):
    if request.method == 'POST':
        form = forms.PredictionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Prepare features for ML model (no feature engineering here)
            features = {
                "pclass": int(data["pclass"]),
                "sex": int(data["sex"]),
                "age": data["age"],
                "sibsp": data["sibsp"],
                "parch": data["parch"],
                "fare": data["fare"],
                "embarked": int(data["embarked"]),
            }

            # ML prediction (feature engineering happens inside ML layer)
            survived, survival_probability = predict_survival(features)

            # Django-side derived fields (for DB storage only)
            family_size = data["sibsp"] + data["parch"] + 1
            is_alone = family_size == 1
            
            # Save prediction to DB
            prediction = Prediction.objects.create(
                pclass=features["pclass"],
                sex=features["sex"],
                age=features["age"],
                fare=features["fare"],
                embarked=features["embarked"],
                family_size=family_size,
                is_alone=is_alone,
                survived=bool(survived),
                survival_probability=survival_probability,
            )

            return redirect("results", prediction_id=prediction.id)
    else:
        form = forms.PredictionForm()

    return render(request, 'prediction_form.html', {'form': form})

def results(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id)
    return render(request, "results.html", {"prediction": prediction})

def history(request):
    predictions = Prediction.objects.order_by("-created_at")
    return render(request, "history.html", {"predictions": predictions})
