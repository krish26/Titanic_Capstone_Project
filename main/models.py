from django.db import models

class Prediction(models.Model):
    # ===== Choices =====
    SEX_CHOICES = [
        (0, "Male"),
        (1, "Female"),
    ]

    EMBARKED_CHOICES = [
        (1, "Cherbourg"),
        (2, "Queenstown"),
        (3, "Southampton"),
    ]
    # ===== Input features from form =====
    pclass = models.IntegerField()
    sex = models.IntegerField(choices=SEX_CHOICES)
    age = models.FloatField()
    fare = models.FloatField()
    embarked = models.IntegerField(choices=EMBARKED_CHOICES)

    family_size = models.IntegerField(null=True, blank=True)
    is_alone = models.BooleanField(default=False)

    # ===== Model output =====
    survived = models.BooleanField()
    survival_probability = models.DecimalField(max_digits=6, decimal_places=4, default=0.0)

    @property
    def probability_percent(self):
        return self.survival_probability * 100

    # ===== Meta =====
    created_at = models.DateTimeField(auto_now_add=True)

    # ===== Label mapping =====
    def alone_label(self):
        return "Yes" if self.is_alone == 1 else "No"

    def __str__(self):
        return f"Prediction #{self.id} | Survived: {self.survived}"
