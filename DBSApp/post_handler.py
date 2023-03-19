from django.db import connection
from DBSApp import input_checks
from DBSApp import raw_query_builder

# Create dict from returned row
def submissions_responsedict(row):
    response = {
        "id": row[0],
        "br_court_name": row[1],
        "kind_name": row[2],
        "cin": row[3],
        "registration_date": row[4],
        "corporate_body_name": row[5],
        "br_section": row[6],
        "br_insertion": row[7],
        "text": row[8],
        "street": row[9],
        "postal_code": row[10],
        "city": row[11]
    }
    return response


def submissions_post(body):
    errors = input_checks.validate_submissions_post(body)
    if errors:
        return {"errors": errors}, 422
    address = body.get("street") + ', ' + body.get("postal_code") + ' ' + body.get("city")
    sql1 = raw_query_builder.submissions_insert_bulletin_query()
    sql2 = raw_query_builder.submissions_insert_raw_query()
    sql3 = raw_query_builder.submissions_insert_podanie_query()
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        bulletin_id = cursor.fetchone()[0]
        cursor.execute(sql2, [bulletin_id])
        raw_id = cursor.fetchone()[0]
        cursor.execute(sql3, [bulletin_id, raw_id, body.get("br_court_name"), body.get("kind_name"),
                              body.get("cin"), body.get("registration_date"), body.get("corporate_body_name"),
                              body.get("br_section"), body.get("br_insertion"), body.get("text"),
                              address, body.get("street"), body.get("postal_code"), body.get("city")])
        response = cursor.fetchone()
    response = submissions_responsedict(response)
    return {"response": response}, 201
