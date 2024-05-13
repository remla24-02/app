import json

from django.http import JsonResponse
from decouple import config
from lib_version_remla24_team02 import VersionUtil
import requests


# TODO: Decide later if we want to add the `v` here, on the frontend, or already on get_version
def version(request):
    return JsonResponse({'version': f"v{VersionUtil.get_version()}"})


def detect(request):
    if request.method == 'POST':
        # Get the url from the frontend request
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')

        # Forward the request to the model-service and get the response (as int) from them
        response = requests.post(f"{config('MODEL_SERVICE_URL')}/predict", json={'url': url})
        prediction = response.json().get('prediction')

        # Convert the prediction into a safe vs phishing detection
        safe = prediction[0] == 0
        return JsonResponse({'safe': safe})
