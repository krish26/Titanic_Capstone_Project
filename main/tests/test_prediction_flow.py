from django.test import TestCase
from django.urls import reverse
from main.models import Prediction

class PredictionFlowTest(TestCase):
    """
        Integration tests for the full prediction workflow.

        Simulates a real user submitting the prediction form,
        verifies DB persistence, redirects, and page rendering.
        """
  
    def setUp(self):
        """
        Runs before each test.

        - prepares reusable URL
        - defines valid test input data
        """

        # Save the form URL for reuse
        self.url = reverse("prediction_form")

        # Simulate real form filling.
        self.valid_data = {
            "pclass": 1,
            "sex": 1,
            "age": 25,
            "sibsp": 0,
            "parch": 0,
            "fare": 100,
            "embarked": 1,
        }

    def test_full_prediction_flow(self):
     
        #Simulate POST request
        response = self.client.post(self.url, data=self.valid_data)

        # Check redirect happened
        self.assertEqual(response.status_code, 302)

        # Check DB saved prediction
        self.assertEqual(Prediction.objects.count(), 1)

        # Get the prediction created by the form submission from the test database
        prediction = Prediction.objects.first()

        # Validate stored fields
        self.assertEqual(prediction.pclass, 1)
        self.assertEqual(prediction.sex, 1)
        self.assertEqual(prediction.age, 25)
        self.assertEqual(prediction.fare, 100)
        self.assertEqual(prediction.embarked, 1)
        self.assertEqual(prediction.family_size, 1)
        self.assertTrue(prediction.is_alone)
        self.assertTrue(prediction.survival_probability >= 0)


    def test_results_page_loads(self):
        #Simulate POST request
        self.client.post(self.url, data=self.valid_data)

        # Get the prediction created by the form submission from the test database
        prediction = Prediction.objects.first()

        # Request the results page for this prediction and verify it loads successfully
        response = self.client.get(reverse("results", args=[prediction.id]))
        self.assertEqual(response.status_code, 200)


    def test_invalid_submission_does_not_create_prediction(self):
        # Simulate bad data input (invalid age)
        bad_data = self.valid_data.copy()
        bad_data["age"] = -10 

        #Simulate POST request with bad_data
        self.client.post(self.url, data=bad_data)

        # Check DB did not save prediction
        self.assertEqual(Prediction.objects.count(), 0)


    def test_prediction_appears_in_history(self):
        #Simulate POST request
        self.client.post(self.url, data=self.valid_data)

        # Request the history page for this prediction and verify it loads successfully
        response = self.client.get(reverse("history"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Prediction")
