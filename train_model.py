import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("Loading dataset...")
data = pd.read_csv('train.csv')

# Selecting 5 impactful features for a clean UI + the target price
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']
target = 'SalePrice'

df = data[features + [target]].copy()

# Handling missing values by filling with the median
df.fillna(df.median(), inplace=True)

X = df[features]
y = df[target]

print("Splitting data and training model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Model trained successfully!")
print(f"Mean Squared Error: {mse:,.2f}")
print(f"R-squared Score: {r2:.4f}")

# Save the trained model
joblib.dump(model, 'house_model.pkl')
print("Model saved as 'house_model.pkl'. Ready for Django!")