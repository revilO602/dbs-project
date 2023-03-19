import datetime

from django.db.models import Max

from DBSApp import input_checks

# Create dict from returned row
from DBSApp.models import BulletinIssues, RawIssues, OrPodanieIssues

def post(body, address_line):
    today = datetime.datetime.now()
    bulletin_data = BulletinIssues.objects.filter(year=today.year)
    number = bulletin_data.aggregate(Max('number')).get('number__max') + 1
    b = BulletinIssues(number=number, year=today.year, published_at=today, created_at=today, updated_at=today)
    b.save()
    r = RawIssues(bulletin_issue_id=b.id, file_name="-", content="-", created_at=today, updated_at=today)
    r.save()
    p = OrPodanieIssues(bulletin_issue_id=b.id, raw_issue_id=r.id, br_mark="-", br_court_code="-",
                        br_court_name=body.get("br_court_name"), kind_code="-", kind_name=body.get("kind_name"),
                        cin=body.get("cin"), registration_date=body.get("registration_date"),
                        corporate_body_name=body.get("corporate_body_name"), br_section=body.get("br_section"),
                        br_insertion=body.get("br_insertion"), text=body.get("text"), created_at=today, updated_at=today,
                        address_line=address_line, street=body.get("street"), postal_code=body.get("postal_code"),
                        city=body.get("city"))
    p.save()
    data = OrPodanieIssues.objects.filter(id=p.id).values('id', 'br_court_name', 'kind_name', 'cin',
                                                        'registration_date', 'corporate_body_name',
                                                        'br_section', 'br_insertion', 'text', 'street',
                                                        'postal_code', 'city')
    return data

def post_submission(body):
    errors = input_checks.validate_submissions_post(body)
    if errors:
        return {"errors": errors}, 422
    address = body.get("street") + ', ' + body.get("postal_code") + ' ' + body.get("city")
    data = post(body, address)
    return {"response": list(data)[0]}, 201

def put_submission(body, id):
    errors = input_checks.validate_put_body(body)
    if errors:
        if errors[0] == "empty":
            return {}, 422
        else: return {"errors": errors}, 422
    obj = OrPodanieIssues.objects.get(id=id)
    for key in body.keys():
        if key == 'br_court_name':
            obj.br_court_name = body.get('br_court_name')
        elif key == 'kind_name':
            obj.kind_name = body.get('kind_name')
        elif key == 'cin':
            obj.cin = body.get('cin')
        elif key == 'registration_date':
            obj.registration_date = body.get('registration_date')
        elif key == 'corporate_body_name':
            obj.corporate_body_name = body.get('corporate_body_name')
        elif key == 'corporate_body_name':
            obj.corporate_body_name = body.get('corporate_body_name')
        elif key == 'br_section':
            obj.br_section = body.get('br_section')
        elif key == 'br_insertion':
            obj.br_insertion = body.get('br_insertion')
        elif key == 'text':
            obj.text = body.get('text')
        elif key == 'street':
            obj.street = body.get('street')
        elif key == 'postal_code':
            obj.postal_code = body.get('postal_code')
        elif key == 'city':
            obj.street = body.get('city')
    obj.save()
    data = OrPodanieIssues.objects.filter(id=obj.id).values('id', 'br_court_name', 'kind_name', 'cin',
                                                          'registration_date', 'corporate_body_name',
                                                          'br_section', 'br_insertion', 'text', 'street',
                                                          'postal_code', 'city')
    return {"response": list(data)[0]}, 201
