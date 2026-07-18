from django.shortcuts import render

# =====================================
# Cost Database (Per Acre)
# =====================================

CROP_COST = {

    "rice": {

        "seed": 2500,
        "fertilizer": 4200,
        "irrigation": 3000,
        "labour": 6000,
        "machinery": 4500

    },

    "maize": {

        "seed": 2200,
        "fertilizer": 3800,
        "irrigation": 2500,
        "labour": 5000,
        "machinery": 4000

    },

    "cotton": {

        "seed": 3000,
        "fertilizer": 5200,
        "irrigation": 3500,
        "labour": 7000,
        "machinery": 5000

    },

    "banana": {

        "seed": 8000,
        "fertilizer": 6500,
        "irrigation": 5000,
        "labour": 9000,
        "machinery": 6000

    },

    "papaya": {

        "seed": 5000,
        "fertilizer": 4500,
        "irrigation": 3500,
        "labour": 7000,
        "machinery": 4500

    },

    "mango": {

        "seed": 10000,
        "fertilizer": 5000,
        "irrigation": 4500,
        "labour": 8500,
        "machinery": 5000

    }

}
# =====================================
# Crop List
# =====================================

crop_list = sorted(CROP_COST.keys())


# =====================================
# Home Page
# =====================================

def cost_home(request):

    context = {
        "crop_list": crop_list
    }

    return render(
        request,
        "cost_estimation/index.html",
        context
    )


# =====================================
# Cost Estimation
# =====================================

def estimate_cost(request):

    context = {
        "crop_list": crop_list
    }

    if request.method == "POST":

        crop = request.POST.get("crop").lower()

        area = float(request.POST.get("area"))

        cost = CROP_COST.get(crop)

        if cost:

            seed_cost = cost["seed"] * area
            fertilizer_cost = cost["fertilizer"] * area
            irrigation_cost = cost["irrigation"] * area
            labour_cost = cost["labour"] * area
            machinery_cost = cost["machinery"] * area

            total_cost = (
                seed_cost +
                fertilizer_cost +
                irrigation_cost +
                labour_cost +
                machinery_cost
            )

            context.update({

                "selected_crop": crop.title(),

                "area": area,

                "seed_cost": seed_cost,

                "fertilizer_cost": fertilizer_cost,

                "irrigation_cost": irrigation_cost,

                "labour_cost": labour_cost,

                "machinery_cost": machinery_cost,

                "total_cost": total_cost

            })

        else:

            context["error"] = "Crop data not available."

    return render(
        request,
        "cost_estimation/index.html",
        context
    )