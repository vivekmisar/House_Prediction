***
```markdown
# House Price Prediction - Setup & Execution Guide

This guide provides step-by-step instructions to clone, set up, and run the Intelligent Property Valuation web application on any local machine.

## Prerequisites
Before you begin, ensure you have the following installed on your system:
* **Python 3.8+** (Add to PATH during installation)
* **Git**

---

## 1. Clone the Repository
Open your terminal (Command Prompt, PowerShell, or Git Bash) and clone the project directory:
```bash
git clone [https://github.com/vivekmisar/House_Prediction.git](https://github.com/vivekmisar/House_Prediction.git)
cd House_Prediction
```

## 2. Set Up a Virtual Environment
It is highly recommended to run this project inside a virtual environment to prevent dependency conflicts.
```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

## 3. Install Dependencies
With your virtual environment activated, install all required machine learning and web frameworks using the provided requirements file:
```bash
pip install -r requirements.txt
```

## 4. Download the Dataset
The machine learning model requires training data. 
1. Go to the [Kaggle Ames Housing Dataset](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data).
2. Download the `train.csv` file.
3. Place `train.csv` directly into the root folder of this project (same level as `manage.py`).

## 5. Train the Machine Learning Model
Generate the Random Forest Regressor model. This script will clean the dataset, train the model, and export it as a serialized `.pkl` file.
```bash
python train_model.py
```
*Note: Wait for the console to print "Model saved!". You should see a new file named `house_model.pkl` appear in your directory.*

## 6. Run the Web Application
Start the Django development server to launch the frontend UI:
```bash
python manage.py runserver
```
Open your web browser and navigate to: **http://127.0.0.1:8000/**

## Troubleshooting
* **Error: `ModuleNotFoundError`**: Ensure your virtual environment is activated and you ran the `pip install` command.
* **Error: `FileNotFoundError: [Errno 2] No such file or directory: 'train.csv'`**: Make sure you downloaded the dataset from Kaggle and placed it in the correct root directory before running `train_model.py`.
```

*** Once you push this Markdown file and your `requirements.txt` to your repo, anyone can pull it down and have it running in 60 seconds flat!