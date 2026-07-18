from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("dashboard.urls")),

    path("crop/", include("cropapp.urls")),

    path("weed/", include("weed_detection.urls")),

    path("pest/", include("pest_detection.urls")),

    path("pesticide/", include("pesticide_recommendation.urls")),

    path("cost/", include("cost_estimation.urls")),

    path("report/", include("advisory.urls")),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )