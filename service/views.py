from django.http import JsonResponse
import json


# TODO: Change to link to model-service
def detect(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')

        # Temporary return information for testing
        safe = True if url == 'true' else False
        return JsonResponse({'safe': safe})
