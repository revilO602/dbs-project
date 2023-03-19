from django.db import connection
from DBSApp import input_checks
from DBSApp import raw_query_builder


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict - taken from django documentation
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictmetadata(page, per_page, total):
    pages = (total // per_page) + (total % per_page > 0)
    return {"page": page,
            "per_page": per_page,
            "pages": pages,
            "total": total}


def submissions_get_result(request):
    page = request.GET.get("page", "1")
    per_page = request.GET.get("per_page", "10")
    query = request.GET.get("query", '')
    reg_date_gte = request.GET.get("registration_date_gte", '')
    reg_date_lte = request.GET.get("registration_date_lte", '')
    order_by = request.GET.get("order_by", 'id')
    order_type = request.GET.get("order_type", "desc")
    # params: (query, query_cin, reg_date_lte, reg_date_gte, page, per_page, order_by, order_type)
    params = input_checks.validate_params(query, reg_date_lte, reg_date_gte,
                                          page, per_page, order_by, order_type, "submissions")
    offset = str(int(params[5]) * (int(params[4]) - 1))
    result_sql = raw_query_builder.submissions_getquery(params[6], params[7], params[2], params[3])
    total_sql = raw_query_builder.submissions_gettotalquery(params[2], params[3])
    with connection.cursor() as cursor:
        cursor.execute(result_sql, [params[0], params[1], offset, params[5]])
        result = dictfetchall(cursor)
        cursor.execute(total_sql, [params[0], params[1]])
        total = cursor.fetchone()[0]
    metadata = dictmetadata(params[4], params[5], total)
    return {"items": result, "metadata": metadata}


def companies_get_result(request):
    page = request.GET.get("page", "1")
    per_page = request.GET.get("per_page", "10")
    query = request.GET.get("query", '')
    last_update_gte = request.GET.get("last_update_gte", '')
    last_update_lte = request.GET.get("last_update_lte", '')
    order_by = request.GET.get("order_by", 'last_update')
    order_type = request.GET.get("order_type", "desc")
    # params: (query, query_cin, date_lte, date_gte, page, per_page, order_by, order_type)
    params = input_checks.validate_params(query, last_update_lte, last_update_gte,
                                          page, per_page, order_by, order_type, "companies")
    result_sql = raw_query_builder.companies_get_query(params[6], params[7], params[2], params[3])
    total_sql = raw_query_builder.companies_get_totalquery(params[2], params[3])
    offset = str(int(params[5]) * (int(params[4]) - 1))
    with connection.cursor() as cursor:
        cursor.execute(result_sql, [params[0], offset, params[5]])
        result = dictfetchall(cursor)
        cursor.execute(total_sql, [params[0]])
        total = cursor.fetchone()[0]
    metadata = dictmetadata(params[4], params[5], total)
    return {"items": result, "metadata": metadata}
