import json

from django.http import HttpResponse, JsonResponse
from decouple import config
from lib_version_remla24_team02 import VersionUtil
from prometheus_client import Counter, Histogram, Gauge, generate_latest

import requests

request_count = Counter('request_count', 'Total number of requests')
request_duration = Histogram('request_duration_milliseconds', 'Duration of request processing in seconds', buckets=[0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.01, 0.1, 1])
phishing_url_count = Counter('phishing_url_count', 'Total number of phishing URLs detected')
safe_url_count = Counter('safe_url_count', 'Total number of safe URLs detected')
prediction_accuracy = Gauge('prediction_accuracy', 'Accuracy of the predictions based on user feedback')
user_feedback_correct = Counter('user_feedback_correct', 'Total number of correct user feedback')
user_feedback_incorrect = Counter('user_feedback_incorrect', 'Total number of incorrect user feedback')

def version(request):
    return JsonResponse({'version': f"v{VersionUtil.get_version()}"})


def detect(request):
    if request.method == 'POST':
        request_count.inc() # Increment request counter

        with request_duration.time(): # Time the request
            # Get the url from the frontend request
            body = json.loads(request.body.decode('utf-8'))
            url = body.get('url')

            # Forward the request to the model-service and get the response (as int) from them
            response = requests.post(f"{config('MODEL_SERVICE_URL')}/api/predict",
                                    headers={'token': config('API_KEY')}, json={'url': url})
            prediction = response.json().get('prediction')

            # Convert the prediction into a safe vs phishing detection
            safe = prediction == 0

            if safe:
                safe_url_count.inc()
            else:
                phishing_url_count.inc()
            
            return JsonResponse({'safe': safe})
        

def feedback(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')
        feedback = body.get('feedback')

        # Update user feedback counters
        if feedback == 'correct':
            user_feedback_correct.inc()
        elif feedback == 'incorrect':
            user_feedback_incorrect.inc()

        # Update prediction accuracy gauge
        correct_count = user_feedback_correct._value.get()
        incorrect_count = user_feedback_incorrect._value.get()
        total_feedback = correct_count + incorrect_count
        if total_feedback > 0:
            prediction_accuracy.set(correct_count / total_feedback)

        return JsonResponse({'status': 'feedback recorded'})

def metrics(request):
    return HttpResponse(generate_latest(), content_type='text/plain')
