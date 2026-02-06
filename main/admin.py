from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pclass', 'sex', 'age', 'fare', 'embarked', 
                    'family_size', 'is_alone', 'survived', 'survival_probability', 'created_at')
    list_filter = ('pclass', 'sex', 'embarked', 'survived', 'is_alone')
    search_fields = ('id', 'sex', 'embarked')
    readonly_fields = ('survived', 'survival_probability', 'created_at')