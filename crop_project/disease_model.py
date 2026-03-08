import random

def predict_disease(image_path):

    diseases = [
        "Healthy",
        "Early Blight",
        "Late Blight",
        "Bacterial Spot"
    ]

    disease = random.choice(diseases)

    confidence = round(random.uniform(85, 98), 2)

    solutions = {
        "Healthy": "No treatment needed. Maintain proper irrigation.",
        "Early Blight": "Apply fungicide and remove infected leaves.",
        "Late Blight": "Use copper-based fungicide immediately.",
        "Bacterial Spot": "Apply antibacterial spray and avoid overhead watering."
    }

    return disease, confidence, solutions[disease]