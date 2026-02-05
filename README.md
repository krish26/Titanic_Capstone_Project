# Titanic_Capstone_Project

## Project overview

This project is a full-stack machine learning application based on the Titanic dataset.  
The goal is to predict whether a passenger survived the Titanic disaster based on passenger information.

## Tech stack

Our tech stack is Python 3.12 for ML and backend, Django 5 for the web app, pandas and scikit-learn for data processing and modeling, SQLite for storing predictions, and Git/GitHub for collaboration, with VS Code as our development environment.

## Team

Krishna Koumudi Koravi, Yuliya Hagberg, Yevheniia Kornilova, Snehal Sanjay Patil, Apeksha Mangalpady

## How to set up and run the project locally

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
- Missing values in Age were filled using the mean age so that we could keep all rows in the dataset.
- The Cabin column was removed because it contains many missing values and did not clearly affect survival.
- Missing values in Embarked were filled with the most common port.
- The Embarked ports were encoded as numbers from 1 to 3 to make them usable for the model.

These choices helped us keep the data clean and easy to work with while preparing it for machine learning.