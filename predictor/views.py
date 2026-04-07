from django.shortcuts import render
import joblib
import os
from django.conf import settings

# Load the model once when the server starts
MODEL_PATH = os.path.join(settings.BASE_DIR, 'house_model.pkl')
model = joblib.load(MODEL_PATH)

def predict_price(request):
    prediction = None
    if request.method == 'POST':
        try:
            # Extract features from the form
            overall_qual = float(request.POST.get('overall_qual'))
            gr_liv_area = float(request.POST.get('gr_liv_area'))
            garage_cars = float(request.POST.get('garage_cars'))
            total_bsmt_sf = float(request.POST.get('total_bsmt_sf'))
            full_bath = float(request.POST.get('full_bath'))
            
            # Format for prediction [OverallQual, GrLivArea, GarageCars, TotalBsmtSF, FullBath]
            input_data = [[overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath]]
            raw_prediction = model.predict(input_data)[0]
            
            # Format the output to a readable currency string
            prediction = f"${raw_prediction:,.2f}"
        except Exception as e:
            prediction = "Error processing input."

    return render(request, 'predictor/index.html', {'prediction': prediction})