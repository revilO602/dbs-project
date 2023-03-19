from dateutil import parser
from django.utils import timezone
from pytz import timezone
from datetime import datetime

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
DEFAULT_QUERY_CIN = -1
DEFAULT_ORDER_BY = {"submissions": 'id', "companies": 'last_update'}
DEFAULT_ORDER_TYPE = 'desc'
REQUIRED_COLUMNS = ['br_court_name', 'kind_name', 'cin', 'registration_date',
                    'corporate_body_name', 'br_section', 'br_insertion', 'text', 'street',
                    'postal_code', 'city']
ORDER_BY_OPTIONS = {"submissions" : ['id', 'br_court_name', 'kind_name', 'cin', 'registration_date',
                    'corporate_body_name', 'br_section', 'br_insertion', 'text', 'street',
                    'postal_code', 'city'],
                    "companies": ["cin", "name", "last_update", "br_section", "address_line",
                                  "or_podanie_issues_count", "znizenie_imania_issues_count",
                                  "likvidator_issues_count", "konkurz_vyrovnanie_issues_count",
                                  "konkurz_restrukturalizacia_actors_count"]
                    }

ORDER_TYPE_OPTIONS = ['desc', 'asc']


def validate_datetime(str_dt):
    if not isinstance(str_dt, str):
        return None
    str_dt.replace("Z", "+00:00")
    try:
        # Can it be parsed to a datetime object?
        dt = parser.isoparse(str_dt)
    except ValueError:
        return None
    if not dt.tzinfo:
        utc = timezone('utc')
        dt = utc.localize(dt)
    return dt


def tz_datetime(input_dt):
    dt = validate_datetime(input_dt)
    if not dt:
        return None
    dt = dt.astimezone(timezone('UTC'))
    return dt


def extract_date(input_dt):
    dt = tz_datetime(input_dt)
    if not dt:
        return None
    date = dt.strftime('%Y-%m-%d')
    return date


def validate_query(query):
    if query.isdigit():
        query_cin = int(query)
    else:
        query_cin = DEFAULT_QUERY_CIN
    query = "%" + query + "%"
    return query, query_cin


def validate_ordering(order_by, order_type, table):
    order_by = order_by.lower()
    order_type = order_type.lower()
    if order_by not in ORDER_BY_OPTIONS.get(table):
        order_by = DEFAULT_ORDER_BY.get(table)
    if order_type not in ORDER_TYPE_OPTIONS:
        order_type = DEFAULT_ORDER_TYPE
    return order_by, order_type

def validate_paging(page, per_page):
    if page.isdigit() and int(page) > 0:
        page = int(page)
    else:
        page = DEFAULT_PAGE
    if per_page.isdigit() and int(per_page) > 0:
        per_page = int(per_page)
    else:
        per_page = DEFAULT_PER_PAGE
    return page, per_page

# Validate all GET parameters
def validate_params(query, date_lte, date_gte, page, per_page, order_by, order_type, table):
    query, query_cin = validate_query(query)
    page, per_page = validate_paging(page, per_page)
    date_lte = extract_date(date_lte)
    date_gte = extract_date(date_gte)
    order_by, order_type = validate_ordering(order_by, order_type, table)
    return query, query_cin, date_lte, date_gte, page, per_page, order_by, order_type


# Validate all GET parameters
def v2_validate_params(date_lte, date_gte, page, per_page, order_by, order_type, table):
    page, per_page = validate_paging(page, per_page)
    date_lte = tz_datetime(date_lte)
    date_gte = tz_datetime(date_gte)
    order_by, order_type = validate_ordering(order_by, order_type, table)
    return date_lte, date_gte, page, per_page, order_by, order_type

# returns error message if cin is wrong, otherwise returns none
def validate_cin(body):
    cin = body.get("cin")
    if isinstance(cin, str):
        if cin.isdigit():
            body["cin"] = int(cin)
            cin = int(cin)
    if isinstance(cin, int):
        if cin < 0:
            return "negative_number"
    else: return "not_number"
    return None


# validates dictionary of parameters in POST request body, if validation finds errors returns list with error dicts
# if no errors are found returns empty list
def validate_submissions_post(body):
    errors = []
    curr_year = datetime.now(timezone('UTC')).year
    for column in REQUIRED_COLUMNS:
        if not body.get(column):
            errors.append({"field": column, "reasons": ["required"]})
        else:
            if column == "cin":
                error = validate_cin(body)
                if error:
                    errors.append({"field": "cin", "reasons": ["required", error]})
            if column == "registration_date":
                date = extract_date(body.get("registration_date"))
                if not date:
                    errors.append({"field": "registration_date", "reasons": ["required", "invalid_range"]})
                else:
                    date_year = int(date.split('-', 1)[0])
                    if curr_year != date_year:
                        errors.append({"field": "registration_date", "reasons": ["required", "invalid_range"]})
                    else: body["registration_date"] = date
    return errors

# Check if at least one key in body is a valid column to update
def validate_put_body(body):
    errors = []
    is_column = False

    for key in body.keys():
        if key in REQUIRED_COLUMNS:
            is_column = True
            break
    if not is_column:
        errors.append("empty")
        return errors

    curr_year = datetime.now(timezone('UTC')).year
    for column in body.keys():
        if column == "cin":
            error = validate_cin(body)
            if error:
                errors.append({"field": "cin", "reasons": [error]})
        if column in REQUIRED_COLUMNS and column != "cin":
            if not isinstance(body.get(column), str):
                errors.append({"field": column, "reasons": ["not_string"]})
        if column == "registration_date":
            date = extract_date(body.get("registration_date"))
            if not date:
                errors.append({"field": "registration_date", "reasons": ["invalid_range"]})
            else:
                date_year = int(date.split('-', 1)[0])
                if curr_year != date_year:
                    errors.append({"field": "registration_date", "reasons": ["invalid_range"]})
                else:
                    body["registration_date"] = date
    return errors
