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
    age = models.FloatField(null=True, blank=True)
    fare = models.FloatField(null=True, blank=True)
    embarked = models.IntegerField(choices=EMBARKED_CHOICES)

    family_size = models.IntegerField(null=True, blank=True)
    is_alone = models.BooleanField(default=False)

    # ===== Model output =====
    survived = models.BooleanField()
    survival_probability = models.FloatField(null=True, blank=True)

    # ===== Meta =====
    created_at = models.DateTimeField(auto_now_add=True)

    # ===== Label mapping =====
    def sex_label(self):
        return "Female" if self.sex == 1 else "Male"

    def embarked_label(self):
        return {
            1: "Cherbourg",
            2: "Queenstown",
            3: "Southampton"
        }.get(self.embarked, "Unknown")
    
    def alone_label(self):
        return "Yes" if self.is_alone == 0 else "No"

    def __str__(self):
        return f"Prediction #{self.id} | Survived: {self.survived}"
