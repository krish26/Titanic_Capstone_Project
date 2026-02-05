from django.shortcuts import render

def index(request):
    return render(request, 'home.html')

def prediction_form(request):
    return render(request, 'prediction_form.html')

def results(request):
    return render(request, 'results.html')

def history(request):
    return render(request, 'history.html')
