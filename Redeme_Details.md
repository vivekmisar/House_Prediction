# Comprehensive Project Documentation: Intelligent Property Valuation

## 1. Project Overview
This project is an end-to-end machine learning web application. It predicts the market value of a house based on its physical attributes. The system uses a **decoupled architecture**:
1. **ML Pipeline (`train_model.py`)**: A standalone Python script that cleans data, trains the model, and exports it.
2. **Web Application (Django)**: A backend server that provides the UI, accepts user input, loads the pre-trained model, and serves the prediction in Indian Rupees (₹).

---

## 2. The Machine Learning Algorithm: Random Forest Regressor

### What is it?
To understand a Random Forest, you first need to understand a **Decision Tree**. A Decision Tree is like a flowchart that asks a series of yes/no questions to arrive at a price (e.g., *Is the house > 2000 sq ft? Yes. Does it have > 1 garage? No.* -> Price = $150k).

A **Random Forest Regressor** is an *ensemble* method. Instead of relying on one single Decision Tree (which might be biased or overfit the training data), a Random Forest creates a "forest" of many different Decision Trees (in this project, 100 trees).

### How it makes a prediction
1. When you input house details, those details are passed to all 100 trees.
2. Each tree calculates its own estimated price.
3. The Random Forest takes the **average** of all 100 predictions to output the final number.

### Why did we choose Random Forest over Linear Regression?
- **Handles non-linearity:** Linear Regression assumes a straight-line relationship between features and price. Real estate does not behave this way (e.g., going from 1 to 2 bathrooms adds huge value, but going from 5 to 6 bathrooms adds very little). Random Forests capture these non-linear relationships.
- **Reduces overfitting:** A single Decision Tree can memorize the training data and perform poorly on new data. By averaging 100 trees trained on random subsets, the Random Forest cancels out individual errors and improves generalization.

---

## 3. The Training Script Breakdown (`train_model.py`)

This file is the engine of the project. Here is what it does, step-by-step:

**Step 1: Data loading and feature selection**
```python
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']
```
Instead of using all 80+ columns from the Kaggle dataset, we select the 5 most significant features. This is **dimensionality reduction via feature selection**. It makes the model faster and keeps the web form simple.

**Step 2: Data preprocessing (imputation)**
```python
df.fillna(df.median(), inplace=True)
```
Real-world data is messy; some rows are missing values (like a blank cell for `GarageCars`). If we feed missing values into the ML algorithm, it fails. `fillna(df.median())` replaces missing values with the median for each column. This is a standard data-cleaning technique.

**Step 3: Train/test split**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
We split the dataset: **80%** for training (`X_train`, `y_train`) and **20%** for testing (`X_test`, `y_test`). The test set is hidden during training and used to measure prediction accuracy.

**Step 4: Model serialization**
```python
joblib.dump(model, 'house_model.pkl')
```
Training a Random Forest takes time. We do not want to retrain the model every time a user clicks "Predict". `joblib.dump` serializes the trained model and saves it as `house_model.pkl`.

---

## 4. The Web Backend Breakdown (Django `views.py`)

The Django view is the bridge between the user's web browser and our ML model.

**Step 1: Loading the Model into Memory**
When the Django server starts, it loads `house_model.pkl` into memory and waits for user input.

**Step 2: Processing the Request**
When the form is submitted (HTTP POST), Django extracts the 5 numbers typed by the user.
```python
input_data = [[overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath]]
raw_prediction_usd = model.predict(input_data)[0]
```
The numbers are formatted into a 2D array (a list inside a list) because `scikit-learn` models can predict multiple houses at once. We pass a single row and extract the first result with `[0]`.

**Step 3: Currency Localization**
Since the Kaggle dataset's target variable (`SalePrice`) was originally tracked in USD, the ML model outputs USD. 
```python
inr_conversion_rate = 83.5 
final_price_inr = raw_prediction_usd * inr_conversion_rate
```
Inside the view, we multiply the raw output by the exchange rate to format the final user-facing output into Indian Rupees (₹), localizing the project for the Indian market.

---

## 5. Quick Q&A for Faculty Defense

- **Faculty:** *"Why didn't you put the model training code inside the Django view?"*
    - **You:** *"That would be inefficient. Training a model is computationally heavy. By decoupling the architecture and using `joblib` to serialize the model, the Django app only performs inference (prediction), which takes milliseconds. This is how production-level ML systems are built."*
- **Faculty:** *"How did you handle missing data in the dataset?"*
    - **You:** *"I used median imputation. During preprocessing, any missing numerical values were replaced with the median of that column. I chose median over mean to avoid skewing the data with outliers."*
- **Faculty:** *"What is R-squared?"* (You will see this printed in your terminal when you train.)
    - **You:** *"R-squared measures the proportion of variance in house price explained by our 5 features. If the score is 0.85, it means our inputs account for 85% of the price variation."*

---

## 6. Glossary (Quick Reference)
- **Overfitting:** When a model memorizes training data and performs poorly on new, unseen data.
- **Imputation:** Filling missing values in a dataset with a reasonable substitute (like the median).
- **R-squared ($R^2$):** A metric that shows how much of the price variation is explained by the model's input features.