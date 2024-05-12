from django.urls import path
from .views import detect, version

urlpatterns = [
    path('detect', detect),
    path('version', version)
]
