from django.db import connection
from django.http import JsonResponse
import json
from DBSApp import get_handler
from DBSApp import post_handler
from DBSApp.raw_query_builder import submissions_delete_query


# Respond with json of uptime
def uptime(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime;")
        row = cursor.fetchone()
    uptime = str(row[0])
    uptime = uptime.replace(',', '')
    return JsonResponse({"psql": {"uptime": uptime}})


# Call functions for GET and POST methods
def submissions_parse_method(request):
    response = dict()
    status_code = 200
    if request.method == "GET":
        response = get_handler.submissions_get_result(request)
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            response, status_code = post_handler.submissions_post(body)
        except json.JSONDecodeError:
            status_code = 400
    else:
        status_code = 404
    return JsonResponse(response, status=status_code)


def submissions_delete(request, id):
    if request.method == "DELETE":
        rawSQL = submissions_delete_query()
        with connection.cursor() as cursor:
            cursor.execute(rawSQL, [id])
            result = cursor.fetchone()
        if not result:
            return JsonResponse({"error": {"message": "Záznam neexistuje"}}, status=404)
        else:
            return JsonResponse({}, status=204)
    return JsonResponse({}, status=404)


def companies_request(request):
    response = {}
    if request.method == "GET":
        response = get_handler.companies_get_result(request)
    return JsonResponse(response)
