from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .models import Prediction
from ML.inference import predict_survival

# Home page view
def index(request):
    return render(request, 'home.html')

# Prediction form view
# Handles BOTH:
# - displaying the form (GET request)
# - processing submitted data (POST request)
def prediction_form(request):

    # If user submitted the form
    if request.method == 'POST':
        form = forms.PredictionForm(request.POST)

         # Validate user input
        if form.is_valid():
            data = form.cleaned_data

            # Prepare features for ML model (convert form data into ML-ready format. No feature engineering here)
            features = {
                "pclass": int(data["pclass"]),
                "sex": int(data["sex"]),
                "age": data["age"],
                "sibsp": data["sibsp"],
                "parch": data["parch"],
                "fare": data["fare"],
                "embarked": int(data["embarked"]),
            }

            # Run ML prediction (feature engineering happens inside ML layer)
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
            # Redirect user to results page
            return redirect("results", prediction_id=prediction.id)
    # GET request → show empty form
    else:
        form = forms.PredictionForm()

    return render(request, 'prediction_form.html', {'form': form})

# Results view
def results(request, prediction_id):
    # Safely fetch prediction or return 404
    prediction = get_object_or_404(Prediction, id=prediction_id)
    return render(request, "results.html", {"prediction": prediction})

# History view
def history(request):
    # Shows all stored predictions (newest first).
    predictions = Prediction.objects.order_by("-created_at")
    return render(request, "history.html", {"predictions": predictions})
