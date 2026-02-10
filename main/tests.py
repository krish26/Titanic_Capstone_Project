from django.test import TestCase
from .forms import PredictionForm
from .models import Prediction

class PredictionFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            "pclass": 1,
            "sex": 0,
            "age": 10,
            "sibsp": 1,
            "parch": 2,
            "fare": 10,
            "embarked": 3,
        }
        form = PredictionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_age(self):
        form_data = {
            "pclass": 1,
            "sex": 0,
            "age": -5,
            "sibsp": 0,
            "parch": 0,
            "fare": 10,
            "embarked": 1,
        }
        form = PredictionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

    def test_invalid_sibsp(self):
            form_data = {
                "pclass": 1,
                "sex": 0,
                "age": 5,
                "sibsp": -1,
                "parch": 0,
                "fare": 10,
                "embarked": 1,
            }
            form = PredictionForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn("sibsp", form.errors)

    def test_invalid_parch(self):
        form_data = {
            "pclass": 1,
            "sex": 0,
            "age": -5,
            "sibsp": 0,
            "parch": -3,
            "fare": 20,
            "embarked": 1,
        }
        form = PredictionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("parch", form.errors)

    def test_invalid_fare(self):
        form_data = {
            "pclass": 1,
            "sex": 0,
            "age": -5,
            "sibsp": 0,
            "parch": 3,
            "fare": -20,
            "embarked": 1,
        }
        form = PredictionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("fare", form.errors)


class PredictionModelTest(TestCase):

    def test_prediction_creation(self):
        prediction = Prediction.objects.create(
            pclass=2,
            sex=1,
            age=20,
            fare=100,
            embarked=1,
            family_size=1,
            is_alone=True,
            survived=False,
            survival_probability=0.10
        )

        self.assertEqual(prediction.pclass, 2)
        self.assertEqual(prediction.sex, 1)
        self.assertEqual(prediction.age, 20)
        self.assertEqual(prediction.fare, 100)
        self.assertEqual(prediction.embarked, 1)
        self.assertEqual(prediction.family_size, 1)
        self.assertTrue(prediction.is_alone)
        self.assertFalse(prediction.survived)
        self.assertEqual(prediction.survival_probability, 0.10)
        self.assertIsNotNone(prediction.created_at)
