from django.test import TestCase
from .forms import PredictionForm

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