from django.shortcuts import render
from . import forms

def index(request):
    return render(request, 'home.html')

def prediction_form(request):
    form = forms.PredictionForm()

    if request.method == 'POST':
        form = forms.PredictionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            return render(request, "results.html", {"data": data})

    return render(request, 'prediction_form.html', {'form': form})

def results(request):
    return render(request, 'results.html')

def history(request):
    return render(request, 'history.html')
