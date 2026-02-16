from django.test import TestCase
from django.urls import reverse
from main.models import Prediction

class PredictionFlowTest(TestCase):
    def test_full_prediction_flow(self):
        # Fake user input 
        form_data = {
            "pclass": 1,
            "sex": 1,
            "age": 25,
            "sibsp": 0,
            "parch": 0,
            "fare": 100,
            "embarked": 1,
        }

        #Simulate POST request
        response = self.client.post(
            reverse("prediction_form"),
            data=form_data
        )

        # Check redirect happened
        self.assertEqual(response.status_code, 302)

        # Check DB saved prediction
        self.assertEqual(Prediction.objects.count(), 1)

        prediction = Prediction.objects.first()

        self.assertEqual(prediction.pclass, 1)
        self.assertEqual(prediction.sex, 1)
        self.assertEqual(prediction.age, 25)
        self.assertEqual(prediction.fare, 100)
        self.assertEqual(prediction.embarked, 1)
        self.assertEqual(prediction.family_size, 1)
        self.assertTrue(prediction.is_alone)
        self.assertTrue(prediction.survival_probability >= 0)