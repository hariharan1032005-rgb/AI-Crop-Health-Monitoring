def predict_pest_risk(temp, humidity, rainfall):

    if temp > 30 and humidity > 70:
        return "High Pest Risk"

    elif temp > 25:
        return "Medium Pest Risk"

    else:
        return "Low Pest Risk"