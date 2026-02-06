from django.db import models

class Prediction(models.Model):
    # ===== Input features from form =====
    pclass = models.IntegerField()
    sex = models.CharField(max_length=10)
    age = models.FloatField(null=True, blank=True)
    fare = models.FloatField(null=True, blank=True)
    embarked = models.CharField(max_length=1)

    family_size = models.IntegerField(null=True, blank=True)
    is_alone = models.BooleanField(default=False)

    # ===== Model output =====
    survived = models.BooleanField()
    survival_probability = models.FloatField(null=True, blank=True)

    # ===== Meta =====
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction #{self.id} | Survived: {self.survived}"
