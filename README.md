# 🏡 Intelligent Property Valuation (House Price Predictor)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-Backend-092E20.svg)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-orange.svg)

An end-to-end Machine Learning web application that predicts real estate market values based on physical property attributes. 

This project implements a **decoupled architecture**, separating the machine learning model training pipeline from the web serving layer to ensure high performance and scalability. 

## ✨ Key Features
* **Advanced ML Engine:** Utilizes an ensemble **Random Forest Regressor** (100 estimators) rather than standard linear models to accurately capture non-linear relationships in real estate data.
* **Decoupled Serving:** The model is pre-trained and serialized via `joblib`. The Django backend performs millisecond-level inference without retraining.
* **Smart Data Processing:** Implements dimensionality reduction (Feature Selection) and handles missing dataset values via median imputation using Pandas.
* **Modern UI/UX:** A responsive, full-screen split layout built with vanilla CSS.
* **Localized Output:** Automatically converts base USD predictions into cleanly formatted Indian Rupees (₹) for the local market.

## 📸 Interface Snapshot
*(Note: Upload your UI screenshot to GitHub and replace this image link!)*
![Project UI Snapshot](https://via.placeholder.com/800x400.png?text=Intelligent+Property+Valuation+Dashboard)

## 🛠️ Technology Stack
* **Machine Learning:** `scikit-learn`, `pandas`, `numpy`, `joblib`
* **Web Framework:** Django
* **Frontend:** HTML5, Vanilla CSS3
* **Dataset:** Kaggle Ames Housing Dataset

## 📚 Project Documentation
To keep the repository clean, detailed information has been split into specific documents:

1. **[Setup & Execution Guide](README-setup.md)**: Step-by-step instructions on how to clone, install dependencies, train the model, and run the server locally.
2. **[Architecture & Algorithm Details](README-details.md)**: A deep dive into the math behind the Random Forest, the data preprocessing steps, and the Django routing logic.

---
*Developed as an academic project demonstrating the integration of predictive machine learning models into functional web applications.*
