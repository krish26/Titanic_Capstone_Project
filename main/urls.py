from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('predict/', views.prediction_form, name='prediction_form'),
    path('history/', views.history, name='history'),
    path('results/<int:prediction_id>/', views.results, name='results'),
]

# Dynamic URLs (like results/<int:prediction_id>/) allow views to fetch and display specific prediction records.
