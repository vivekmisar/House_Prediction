
# Comprehensive Project Documentation: Intelligent Property Valuation

## 1. Project Overview
This project is an end-to-end Machine Learning web application. It predicts the market value of a house based on its physical attributes. The system is built using a **decoupled architecture**:
1.  **The ML Pipeline (`train_model.py`)**: A standalone Python script that cleans data, trains the mathematical model, and exports it.
2.  **The Web Application (Django)**: A backend server that provides a user interface, accepts user input, loads the pre-trained model, and serves the prediction in Indian Rupees (₹).

---

## 2. The Machine Learning Algorithm: Random Forest Regressor

### What is it?

To understand a Random Forest, you first need to understand a **Decision Tree**. A Decision Tree is like a flowchart that asks a series of yes/no questions to arrive at a price. (e.g., *Is the house > 2000 sq ft? Yes. Does it have > 1 garage? No.* -> Price = $150k).

A **Random Forest Regressor** is an *ensemble* method. Instead of relying on one single Decision Tree (which might be biased or over-memorize the training data), a Random Forest creates a "forest" of many different Decision Trees (in our case, 100 trees). 

### How it makes a prediction:
1.  When you input house details, those details are passed to all 100 trees.
2.  Every single tree calculates its own estimated price.
3.  The Random Forest takes the **average** of all 100 predictions to output the final number.

### Why did we choose Random Forest over Linear Regression?
* **Handles Non-Linearity:** Linear Regression assumes a perfectly straight-line relationship between features and price. Real estate doesn't work like that (e.g., going from 1 to 2 bathrooms adds huge value, but going from 5 to 6 bathrooms adds very little). Random Forests naturally capture these non-linear relationships.
* **Prevents Overfitting:** A single Decision Tree tends to "memorize" the training data and performs poorly on new data. By averaging 100 trees trained on random subsets of the data, the Random Forest cancels out individual errors, making it highly accurate and robust.

---

## 3. The Training Script Breakdown (`train_model.py`)

This file is the engine of the project. Here is exactly what it does, step-by-step:

**Step 1: Data Loading & Feature Selection**
```python
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']
```
Instead of overwhelming the model (and the user) with all 80 columns from the Kaggle dataset, we selected the top 5 most statistically significant features. This is called **Dimensionality Reduction via Feature Selection**. It makes the model faster and the web form user-friendly.

**Step 2: Data Preprocessing (Imputation)**
```python
df.fillna(df.median(), inplace=True)
```
Real-world data is messy; some houses in the CSV might be missing values (like a blank cell for GarageCars). If we feed blank cells into the ML algorithm, it crashes. `fillna(df.median())` finds the missing spots and replaces them with the median value of that column. This is a standard data science cleaning technique.

**Step 3: Train/Test Split**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
We divide our dataset. **80%** of the houses are used to teach the model (`X_train`, `y_train`). The remaining **20%** (`X_test`, `y_test`) are hidden from the model during training. After training, we test the model on this 20% to see how accurately it predicts prices for houses it has never seen before.

**Step 4: Model Serialization**
```python
joblib.dump(model, 'house_model.pkl')
```
Training a Random Forest takes computational power and time. We do not want to retrain the model every single time a user clicks "Predict" on the website. `joblib.dump` translates our trained mathematical model into a byte-stream and saves it as a physical file (`house_model.pkl`).

---

## 4. The Web Backend Breakdown (Django `views.py`)

The Django view is the bridge between the user's web browser and our ML model.

**Step 1: Loading the Model into Memory**
When the Django server starts, it reads `house_model.pkl` into the server's RAM. It waits idly until a user submits the form.

**Step 2: Processing the Request**
When the form is submitted (HTTP POST), Django extracts the 5 numbers typed by the user.
```python
input_data = [[overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath]]
raw_prediction_usd = model.predict(input_data)[0]
```
The numbers are formatted into a 2D Array (a list inside a list) because `scikit-learn` models are built to predict multiple houses at once. We pass our single house in, and extract the first result `[0]`.

**Step 3: Currency Localization**
Since the Kaggle dataset's target variable (`SalePrice`) was originally tracked in USD, the ML model outputs USD. 
```python
inr_conversion_rate = 83.5 
final_price_inr = raw_prediction_usd * inr_conversion_rate
```
Inside the view, we multiply the raw ML output by the current exchange rate to format the final user-facing output into Indian Rupees (₹), localizing the project for the Indian market.

---

## 5. Quick Q&A for Faculty Defense

* **Faculty:** *"Why didn't you put the model training code inside the Django view?"*
    * **You:** *"That would be highly inefficient. Training a model is computationally heavy. By decoupling the architecture and using `joblib` to serialize the model, the Django app only performs inference (prediction), which takes milliseconds. This is how production-level ML systems are built."*
* **Faculty:** *"How did you handle missing data in the dataset?"*
    * **You:** *"I used median imputation. During the preprocessing phase in Pandas, any missing numerical features were replaced with the median value of that feature's column. I chose median over mean to avoid skewing the data via extreme outliers."*
* **Faculty:** *"What is R-squared?"* (You will see this printed in your terminal when you train).
    * **You:** *"R-squared is a statistical measure that represents the proportion of the variance in the house price that is explained by our 5 features. If the score is 0.85, it means our model's inputs account for 85% of the reason the price moves up or down."*