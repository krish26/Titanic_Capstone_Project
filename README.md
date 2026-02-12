# Titanic_Capstone_Project

## Project overview

This project is a full-stack machine learning application based on the Titanic dataset.  
The goal is to predict whether a passenger survived the Titanic disaster based on passenger information.

The project covers the complete machine learning workflow:
- Data exploration and preprocessing
- Feature engineering
- Model training and evaluation
- Deployment of the model in a Django web application
- Database persistence of predictions
- Collaborative development using Git and Scrum practices

The purpose of this project is to demonstrate how a machine learning model can be integrated into a full-stack web application. The focus is not only on model performance, but also on data processing, system design, and presenting predictions through a user-friendly interface.

## Tech stack

Our tech stack is Python 3.12 for ML and backend, Django 5 for the web app, pandas and scikit-learn for data processing and modeling, SQLite for storing predictions, and Git/GitHub for collaboration, with VS Code as our development environment.

## Team

Krishna Koumudi Koravi, Yuliya Hagberg, Yevheniia Kornilova, Snehal Sanjay Patil, Apeksha Mangalpady

## Dataset

The project uses the **Titanic dataset** provided by Kaggle: https://www.kaggle.com/c/titanic/data

## How to set up and run the project locally

The following instructions explain how to run the project locally for development and testing.

### 1. Clone the repo
```bash
git clone https://github.com/krish26/Titanic_Capstone_Project.git
cd Titanic_Capstone_Project
```

### 2. Create and activate a venv
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Run the server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

### 6. Pulling future changes
```bash
git pull
pip install -r requirements.txt   # only needed if dependencies changed
python manage.py migrate          # only if models changed
```

## Data Processing Decisions

We made a few simple decisions to handle missing and categorical data:
- Missing values in `Age` were filled using the mean age so that we could keep all rows in the dataset.
- The `Cabin` column was removed because it contains many missing values and did not clearly affect survival.
- Encode Categorical Variable (`Sex`) by conveting it into numerical format as (female= 1, male= 0).
- Missing values in `Embarked` were filled with the most common port.
- The `Embarked` ports were encoded as numbers from 1 to 3 to make them usable for the model.

These choices helped us keep the data clean and easy to work with while preparing it for machine learning.

## Feature Engineering

The following features were engineered to improve model performance while keeping the dataset interpretable:

### **AgeGroup**
Ages are binned into life-stage categories (Child, Teen, YoungAdult, Adult, Senior) to capture non-linear survival patterns.

#### Why we do this
Titanic survival isn’t linear with age:
- Children were prioritized for lifeboats
- Elderly had lower survival
- Binning simplifies the pattern, making it easier for models to learn survival trends.

### **FareGroup**
Ticket fares are grouped into quartiles (Low → VeryHigh) to represent socio-economic status and reduce skewness.

#### Why we do this
- Fare distribution is heavily skewed (few very expensive tickets).

### **Quantile binning**
- Reduces the effect of extreme outliers
- Turns fare into socio-economic categories that better capture survival patterns
- Models can now learn that higher fare → higher survival probability without being dominated by extreme values.

### **FamilySize**
Total number of family members traveling together (`SibSp` + `Parch` + 1).

### **IsAlone**
Binary feature indicating whether a passenger was traveling alone.

These features help models learn survival patterns related to age priority, wealth, and group dynamics.

## Description of the machine learning model
This project uses supervised machine learning models to predict whether a passenger survived the Titanic disaster. The target variable is Survived, which is a binary classification problem (survived or not survived).

### Data preparation
Before training the models, the dataset was preprocessed as follows:
- Unused or non-informative columns such as `PassengerId`, `Name`, `Ticket`, and `Cabin` were removed.
- Missing values were handled during preprocessing.
- Categorical features such as `AgeGroup` and `FareGroup` were converted into numerical format using one-hot encoding.
- The dataset was split into training and testing sets using an 80/20 split.

### Logistic Regression
A Logistic Regression model was trained as a baseline classifier.
- Logistic Regression is a simple and interpretable model commonly used for binary classification tasks.
- The model was trained using scikit-learn’s LogisticRegression with an increased maximum number of iterations to ensure convergence.
- Model performance was evaluated using accuracy, confusion matrix, precision, recall, and F1-score.

The Logistic Regression model achieved an accuracy of approximately **81,6%** on the test set, providing a strong and interpretable baseline.

### Random Forest
A Random Forest classifier was also trained to capture more complex patterns in the data.
- Random Forest is an ensemble model that combines multiple decision trees to improve prediction accuracy and reduce overfitting.
- The model was trained with tuned hyperparameters such as the number of trees, tree depth, and minimum samples per split.
- Model performance was evaluated using accuracy, confusion matrix, precision, recall, and F1-score.

The Random Forest model achieved an accuracy of approximately **83,2%**. While the accuracy was quite similar to Logistic Regression, Random Forest demonstrated better flexibility in modeling non-linear feature interactions.

### Model selection
Both models were trained and evaluated to compare performance and interpretability:
- Logistic Regression was used as a baseline model due to its simplicity and transparency.
- Random Forest was selected as the final model due to its better predictive performance.

The trained model is saved and integrated into the Django web application to generate survival predictions based on user input.

## System architecture overview

The system follows a simple full-stack architecture that connects a machine learning workflow with a web application.

1. **Front-end (Django templates & Bootstrap)**  
   Users interact with the application through HTML forms styled with Bootstrap. The prediction form collects passenger information such as class, age, sex, fare, and embarkation port.

2. **Back-end (Django views & forms)**  
   Django handles form validation, feature engineering, and application logic. After the form is submitted, the backend prepares the input data for the machine learning model.

3. **Machine learning (pandas & scikit-learn)**  
   A trained machine learning model is used to predict survival probability based on the processed input features.

4. **Database (SQLite)**  
   Each prediction, along with the input features and model output, is stored in a SQLite database. This allows predictions to be reviewed later on the History page.

5. **Results and history pages**  
   The prediction result is shown immediately after submission and all past predictions can be viewed in a dedicated history view.

## Unittest

To ensure reliability and correctness, unit tests were implemented using Django’s built-in testing framework (based on Python’s `unittest`).
The test suite covers the following components:

### Form validation tests
The `PredictionForm` is tested to ensure proper validation of user input. Tests include:
- Valid form submission
- Negative or invalid values for age, sibsp, parch, and fare
- Missing required fields

These tests verify that incorrect input is properly rejected and that validation rules work as expected.

### Model tests
The `Prediction` model is tested to confirm:
- Objects can be successfully created
- All fields are stored correctly
- The `created_at` timestamp is automatically generated

This ensures database integrity and correct model behavior.

### View tests
View tests verify that:
- The home page loads successfully
- The prediction form page loads correctly
- The history page loads correctly
- Submitting the prediction form creates a new `Prediction` object in the database

These tests validate the full request–response cycle and confirm that the application behaves correctly from a user perspective.

### Running tests

To run the test suite locally:

```bash
python manage.py test
```