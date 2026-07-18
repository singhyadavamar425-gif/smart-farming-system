from django.shortcuts import render

# ======================================
# Pesticide Recommendation Database
# ======================================

PESTICIDES = {

    ("rice","stem_borer"): {
        "pesticide":"Cartap Hydrochloride",
        "dosage":"10 kg/acre",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Wear gloves while spraying."
    },

    ("rice","aphids"): {
        "pesticide":"Imidacloprid",
        "dosage":"0.3 ml/L",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Avoid spraying during rain."
    },

    ("maize","armyworm"): {
        "pesticide":"Chlorantraniliprole",
        "dosage":"0.4 ml/L",
        "spray_time":"Evening",
        "organic":"BT Spray",
        "precaution":"Keep away from ponds."
    },

    ("maize","grasshopper"): {
        "pesticide":"Malathion",
        "dosage":"1 ml/L",
        "spray_time":"Morning",
        "organic":"Neem Extract",
        "precaution":"Wear mask."
    },

    ("cotton","bollworm"): {
        "pesticide":"Emamectin Benzoate",
        "dosage":"220 g/acre",
        "spray_time":"Evening",
        "organic":"Neem Oil",
        "precaution":"Keep away from children."
    },

    ("cotton","aphids"): {
        "pesticide":"Imidacloprid",
        "dosage":"0.5 ml/L",
        "spray_time":"Morning",
        "organic":"Soap Spray",
        "precaution":"Wear gloves."
    },

    ("banana","mites"): {
        "pesticide":"Abamectin",
        "dosage":"0.5 ml/L",
        "spray_time":"Morning",
        "organic":"Garlic Spray",
        "precaution":"Use protective clothing."
    },

    ("banana","beetle"): {
        "pesticide":"Carbaryl",
        "dosage":"2 g/L",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Avoid over spraying."
    },

    ("papaya","aphids"): {
        "pesticide":"Dimethoate",
        "dosage":"1 ml/L",
        "spray_time":"Morning",
        "organic":"Neem Extract",
        "precaution":"Wear mask."
    },

    ("apple","mites"): {
        "pesticide":"Abamectin",
        "dosage":"0.5 ml/L",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Wear gloves."
    },

    ("mango","fruit_fly"): {
        "pesticide":"Spinosad",
        "dosage":"0.5 ml/L",
        "spray_time":"Evening",
        "organic":"Fruit Fly Trap",
        "precaution":"Collect fallen fruits."
    },

    ("orange","aphids"): {
        "pesticide":"Imidacloprid",
        "dosage":"0.3 ml/L",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Avoid rain."
    },

    ("grapes","mites"): {
        "pesticide":"Sulphur",
        "dosage":"2 g/L",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Do not mix with oil spray."
    },

    ("watermelon","aphids"): {
        "pesticide":"Thiamethoxam",
        "dosage":"0.3 g/L",
        "spray_time":"Morning",
        "organic":"Neem Oil",
        "precaution":"Use gloves."
    },

    ("chickpea","armyworm"): {
        "pesticide":"Chlorpyrifos",
        "dosage":"2 ml/L",
        "spray_time":"Evening",
        "organic":"Neem Extract",
        "precaution":"Keep away from livestock."
    }

}
# ======================================
# Crop List
# ======================================

crop_list = sorted(list(set([item[0] for item in PESTICIDES.keys()])))


# ======================================
# Pest List
# ======================================

pest_list = sorted(list(set([item[1] for item in PESTICIDES.keys()])))

# ======================================
# Home Page
# ======================================

def pesticide_home(request):

    context = {
        "crop_list": crop_list,
        "pest_list": pest_list,
    }

    return render(
        request,
        "pesticide_recommendation/index.html",
        context
    )

# ======================================
# Recommendation Function
# ======================================

def recommend_pesticide(request):

    context = {

        "crop_list": crop_list,
        "pest_list": pest_list

    }

    if request.method == "POST":

        crop = request.POST.get("crop").lower()

        pest = request.POST.get("pest").lower()

        result = PESTICIDES.get((crop, pest))

        if result:

            context.update({

                "selected_crop": crop.title(),

                "selected_pest": pest.title(),

                "pesticide": result["pesticide"],

                "dosage": result["dosage"],

                "spray_time": result["spray_time"],

                "organic": result["organic"],

                "precaution": result["precaution"]

            })

        else:

            context["error"] = "No recommendation available for this Crop and Pest."

    return render(
        request,
        "pesticide_recommendation/index.html",
        context
    )