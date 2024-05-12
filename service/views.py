from django.http import JsonResponse
import json
from lib_version_remla24_team02 import VersionUtil


# TODO: Decide later if we want to add the `v` here, on the frontend, or already on get_version
def version(request):
    return JsonResponse({'version': f"v{VersionUtil.get_version()}"})


# TODO: Change to link to model-service
def detect(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')

        # Temporary return information for testing
        safe = True if url == 'true' else False
        return JsonResponse({'safe': safe})
