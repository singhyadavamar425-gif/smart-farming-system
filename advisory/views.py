from django.shortcuts import render

def advisory_home(request):

    context = {

        # Crop Recommendation
        "crop": "Rice",
        "confidence": "95.60 %",
        "soil": "Clay Soil",
        "fertilizer": "Urea + DAP",
        "gdd": "2200",

        # Weed Detection
        "weed": "Parthenium",
        "weed_confidence": "98.40 %",

        # Pest Detection
        "pest": "Stem Borer",
        "pest_confidence": "97.20 %",

        # Pesticide Recommendation
        "pesticide": "Cartap Hydrochloride",
        "dosage": "10 kg/acre",
        "spray_time": "Morning",
        "organic": "Neem Oil",

        # Cost Estimation
        "seed_cost": 2500,
        "fertilizer_cost": 4200,
        "labour_cost": 6000,
        "machinery_cost": 4500,
        "irrigation_cost": 3000,
        "total_cost": 20200,

    }

    return render(
        request,
        "advisory/index.html",
        context
    )