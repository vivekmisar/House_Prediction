from django.shortcuts import render
import joblib
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'house_model.pkl')
model = joblib.load(MODEL_PATH)

def number_to_words(n: int) -> str:
    if n == 0:
        return 'zero'

    ones = (
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
        'seventeen', 'eighteen', 'nineteen'
    )
    tens = ('', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety')
    scales = (
        (10_000_000, 'crore'),
        (100_000, 'lakh'),
        (1_000, 'thousand'),
        (100, 'hundred'),
    )

    def two_digit_words(x: int) -> str:
        if x < 20:
            return ones[x]
        return tens[x // 10] + ('' if x % 10 == 0 else f"-{ones[x % 10]}")

    words = []
    remaining = n

    for scale_value, scale_name in scales:
        if remaining >= scale_value:
            scale_count = remaining // scale_value
            remaining %= scale_value

            if scale_value == 100:
                words.append(f"{ones[scale_count]} {scale_name}")
            else:
                words.append(f"{number_to_words(scale_count)} {scale_name}")

    if remaining > 0:
        words.append(two_digit_words(remaining))

    return ' '.join(words).strip()

def predict_price(request):
    prediction = None
    amount_in_words = None
    form_values = {
        'overall_qual': '7',
        'gr_liv_area': '2000',
        'garage_cars': '2',
        'total_bsmt_sf': '800',
        'full_bath': '2',
    }
    if request.method == 'POST':
        try:
            form_values = {
                'overall_qual': request.POST.get('overall_qual', form_values['overall_qual']),
                'gr_liv_area': request.POST.get('gr_liv_area', form_values['gr_liv_area']),
                'garage_cars': request.POST.get('garage_cars', form_values['garage_cars']),
                'total_bsmt_sf': request.POST.get('total_bsmt_sf', form_values['total_bsmt_sf']),
                'full_bath': request.POST.get('full_bath', form_values['full_bath']),
            }

            overall_qual = float(form_values['overall_qual'])
            gr_liv_area = float(form_values['gr_liv_area'])
            garage_cars = float(form_values['garage_cars'])
            total_bsmt_sf = float(form_values['total_bsmt_sf'])
            full_bath = float(form_values['full_bath'])
            
            input_data = [[overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath]]
            raw_prediction_usd = model.predict(input_data)[0]
            
            # Convert USD to INR
            inr_conversion_rate = 83.5 
            final_price_inr = raw_prediction_usd * inr_conversion_rate
            rounded_price_inr = int(round(final_price_inr))
            
            # Format nicely with commas (Indian numbering system)
            prediction = f"₹ {rounded_price_inr:,.0f}"
            amount_in_words = f"{number_to_words(rounded_price_inr)} rupees"
        except Exception as e:
            prediction = "Error processing input."
            amount_in_words = None

    return render(
        request,
        'predictor/index.html',
        {
            'prediction': prediction,
            'amount_in_words': amount_in_words,
            'form_values': form_values,
        },
    )