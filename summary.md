# Project Summary: Intelligent Property Valuation (House Price Predictor)

## 1. Project Overview
The **Intelligent Property Valuation** project is an end-to-end Machine Learning web application designed to predict real estate market values based on physical property attributes. It uses a **decoupled architecture**, meaning the machine learning model training pipeline is entirely separated from the web application that serves the predictions. This decoupling ensures high performance, allowing the web server to make millisecond-level inferences using a pre-trained model without the computational overhead of retraining.

## 2. Technology Stack
* **Machine Learning:** `scikit-learn`, `pandas`, `numpy`, `joblib`
* **Web Framework:** Django (Backend)
* **Frontend:** HTML5, Vanilla CSS3
* **Dataset:** Kaggle Ames Housing Dataset

## 3. The Dataset and Features
The model is trained on the Kaggle Ames Housing Dataset. While the original dataset contains over 80 columns, the project employs **dimensionality reduction via feature selection** to isolate the 5 most significant predictors:
1. `OverallQual`: Overall material and finish quality
2. `GrLivArea`: Above grade (ground) living area square feet
3. `GarageCars`: Size of garage in car capacity
4. `TotalBsmtSF`: Total square feet of basement area
5. `FullBath`: Full bathrooms above grade

**Data Preprocessing:** Missing values within the dataset are handled using **median imputation** (`df.fillna(df.median())`), replacing missing cells with the median of that specific column to maintain data integrity without skewing the distribution.

## 4. AI and Machine Learning Concepts Used

### 4.1. The Algorithm: Random Forest Regressor
The project utilizes an ensemble learning algorithm called the **Random Forest Regressor** (configured with 100 estimators/trees). 

* **Decision Trees:** The foundation of the algorithm, acting like a flowchart of yes/no questions based on features to arrive at a price estimate.
* **Ensemble Method:** Instead of relying on a single decision tree which is prone to **overfitting** (memorizing training data but failing on new data), the Random Forest creates 100 distinct decision trees. 
* **Prediction Mechanism:** Each tree makes an independent prediction. The model then averages these 100 predictions to output a final, highly accurate house value.
* **Why Random Forest?** It efficiently captures non-linear relationships in real estate pricing (e.g., the diminishing returns of adding a 6th bathroom compared to a 2nd) far better than a simple Linear Regression model.

### 4.2. Key ML Terminology in the Project
* **Feature Selection (Dimensionality Reduction):** The process of selecting a subset of relevant features (the 5 columns) for use in model construction to simplify the model and improve performance.
* **Train/Test Split:** The dataset is divided into two sets: 80% for training the model (`X_train`, `y_train`) and 20% reserved for testing its accuracy on unseen data (`X_test`, `y_test`).
* **Imputation:** A data cleaning technique used to handle missing data by substituting missing values with the column's median.
* **Serialization (`joblib`):** The process of exporting and saving the trained model (`house_model.pkl`) so it can be loaded into the Django web server for quick predictions without retraining.
* **R-squared ($R^2$) and MSE:** Statistical measures used in the training script to evaluate how well the model's predictions fit the actual data. $R^2$ represents the proportion of the variance in the target variable (house price) that is predictable from the input features.
* **Overfitting:** A modeling error where a machine learning model learns the training data too well, failing to generalize to new, unseen data (which Random Forest helps mitigate).

## 5. Web Serving and Inference
In the Django backend (`views.py`), the pre-trained `house_model.pkl` is loaded into memory. When a user submits property details via the web form, the Django view processes the input as a 2D array, uses the model to perform the prediction, and converts the raw USD output into **Indian Rupees (₹)** based on a predefined exchange rate, providing a locally relevant result for the user.
