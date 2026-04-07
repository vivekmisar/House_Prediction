import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("Loading dataset...")
data = pd.read_csv('train.csv')

features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']
target = 'SalePrice'

df = data[features + [target]].copy()
df.fillna(df.median(), inplace=True)

X = df[features]
y = df[target]

print("Splitting data and training Random Forest model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Using Random Forest (An ensemble of Decision Trees - safe but impressive)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Model trained successfully!")
print(f"R-squared Score: {r2:.4f}")

joblib.dump(model, 'house_model.pkl')
print("Model saved! Run this script to update the .pkl file.")