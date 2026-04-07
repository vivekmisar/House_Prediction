# House Price Prediction - Setup Guide

Follow these steps to set up and run the Intelligent Property Valuation web app locally.

## Prerequisites
- Python 3.8+ (add to PATH during installation)
- Git

## 1) Clone the repository
Open Command Prompt, PowerShell, or Git Bash:
```bash
git clone https://github.com/vivekmisar/House_Prediction.git
cd House_Prediction
```

## 2) Create and activate a virtual environment
```bash
python -m venv venv
```
Activate it:

Windows:
```bash
.\venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

## 3) Install dependencies
```bash
pip install -r requirements.txt
```

## 4) Download the dataset
1. Go to the Kaggle Ames Housing Dataset: https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data
2. Download `train.csv`.
3. Place `train.csv` in the project root (same folder as `manage.py`).

## 5) Train the model
This creates `house_model.pkl`:
```bash
python train_model.py
```
Wait for the message "Model saved!" and confirm the file appears in the root folder.

## 6) Run the web app
```bash
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

## Troubleshooting
- `ModuleNotFoundError`: activate the virtual environment, then run `pip install -r requirements.txt`.
- `FileNotFoundError: train.csv`: confirm the file is in the project root before running `train_model.py`.