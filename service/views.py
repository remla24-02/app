import json

from django.http import HttpResponse, JsonResponse
from decouple import config
from lib_version_remla24_team02 import VersionUtil
from prometheus_client import Counter, generate_latest

import requests

request_count = Counter('request_count', 'Total number of requests')

def version(request):
    return JsonResponse({'version': f"v{VersionUtil.get_version()}"})


def detect(request):
    if request.method == 'POST':
        request_count.inc()

        # Get the url from the frontend request
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')

        # Forward the request to the model-service and get the response (as int) from them
        response = requests.post(f"{config('MODEL_SERVICE_URL')}/api/predict",
                                 headers={'token': config('API_KEY')}, json={'url': url})
        prediction = response.json().get('prediction')

        # Convert the prediction into a safe vs phishing detection
        safe = prediction == 0
        return JsonResponse({'safe': safe})

def metrics(request):
    return HttpResponse(generate_latest(), content_type='text/plain')
