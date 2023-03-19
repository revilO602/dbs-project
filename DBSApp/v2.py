import json
from django.http import JsonResponse
from DBSApp import v2_get_handler, v2_post_handler

# Call functions for GET and POST methods
from DBSApp.models import OrPodanieIssues


def parse_method(request):
    response = dict()
    status_code = 200
    if request.method == "GET":
        response = v2_get_handler.get_submissions(request)
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            response, status_code = v2_post_handler.post_submission(body)
        except json.JSONDecodeError:
            status_code = 400
    else:
        status_code = 404
    return JsonResponse(response, status=status_code)


def parse_method_id(request, id):
    response = dict()
    status_code = 200
    if request.method == "GET":
        response, status_code = v2_get_handler.get_submission_id(id)
    elif request.method == "PUT":
        try:
            body = json.loads(request.body)
            response, status_code = v2_post_handler.put_submission(body, id)
        except json.JSONDecodeError:
            status_code = 422
        except OrPodanieIssues.DoesNotExist:
            status_code = 404
    elif request.method == "DELETE":
        response, status_code = delete_submission_id(id)
    else:
        status_code = 404
    return JsonResponse(response, status=status_code)


def delete_submission_id(id):
    data = OrPodanieIssues.objects.filter(id=id)
    if data:
        data.delete()
        return {}, 204
    else:
        return {"error": {"message": "Záznam neexistuje"}}, 404

def companies_request(request):
    response = {}
    if request.method == "GET":
        response = v2_get_handler.get_companies(request)
    return JsonResponse(response)

