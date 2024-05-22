from django.urls import path
from .views import detect, version, feedback

urlpatterns = [
    path('detect', detect),
    path('version', version),
    path('feedback', feedback)
]
