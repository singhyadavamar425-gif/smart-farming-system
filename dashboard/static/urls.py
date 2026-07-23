from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve

urlpatterns = [
    # ... baki routes ...
    path('manifest.json', serve, {'path': 'manifest.json'}),
    path('serviceworker.js', serve, {'path': 'serviceworker.js'}),
]