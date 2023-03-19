from typing import List

from django.db.models import Q, Count, Value as V, F, Subquery, OuterRef
from django.db.models.functions import Concat

from DBSApp import input_checks
from DBSApp.models import Companies, OrPodanieIssues, LikvidatorIssues, KonkurzVyrovnanieIssues, ZnizenieImaniaIssues, \
    KonkurzRestrukturalizaciaActors
from DBSApp.get_handler import dictmetadata


def get(query, params, offset):
    if query.isdigit():
        query_cin = int(query)
    else:
        query_cin = -1
    data = OrPodanieIssues.objects.annotate(search_string=Concat('corporate_body_name', V(' '), 'city'))
    data = data.filter(Q(search_string__icontains=query) | Q(cin__exact=query_cin))
    if params[0]:
        data = data.filter(registration_date__lte=params[0])
    if params[1]:
        data = data.filter(registration_date__gte=params[1])
    if params[5] == "asc":
        data = data.order_by(F(params[4]).asc(nulls_last=True))
    else:
        data = data.order_by(F(params[4]).desc(nulls_last=True))
    return data.count(), data[offset:int(params[3]) + offset].values('id', 'br_court_name', 'kind_name', 'cin',
                                                                     'registration_date', 'corporate_body_name',
                                                                     'br_section', 'br_insertion', 'text', 'street',
                                                                     'postal_code', 'city')


def get_submissions(request):
    page = request.GET.get("page", "1")
    per_page = request.GET.get("per_page", "10")
    query = request.GET.get("query", '')
    reg_date_gte = request.GET.get("registration_date_gte", '')
    reg_date_lte = request.GET.get("registration_date_lte", '')
    order_by = request.GET.get("order_by", 'id')
    order_type = request.GET.get("order_type", "desc")
    # params: (reg_date_lte, reg_date_gte, page, per_page, order_by, order_type)
    params = input_checks.v2_validate_params(reg_date_lte, reg_date_gte,
                                             page, per_page, order_by, order_type, "submissions")
    offset = int(params[3]) * (int(params[2]) - 1)
    count, data = get(query, params, offset)
    metadata = dictmetadata(params[2], params[3], count)
    return {"items": list(data), "metadata": metadata}


def get_submission_id(id):
    data = OrPodanieIssues.objects.filter(id=id).values('id', 'br_court_name', 'kind_name', 'cin',
                                                     'registration_date', 'corporate_body_name',
                                                     'br_section', 'br_insertion', 'text', 'street',
                                                     'postal_code', 'city')
    if data:
        return {"response": list(data)[0]}, 200
    else: return {"response": {}}, 404


def get_comp(query, params, offset):
    data = Companies.objects.annotate(search_string=Concat('name', V(' '), 'address_line'))
    data = data.filter(search_string__icontains=query)
    if params[0]:
        data = data.filter(last_update__lte=params[0])
    if params[1]:
        data = data.filter(last_update__gte=params[1])

    or_podanie_issues_count = OrPodanieIssues.objects.filter(company_id=OuterRef('cin')).order_by().values(
        'company_id')
    or_podanie_issues_count = or_podanie_issues_count.annotate(count=Count('*')).values('count')
    data = data.annotate(or_podanie_issues_count=Subquery(or_podanie_issues_count))

    znizenie_imania_issues_count = ZnizenieImaniaIssues.objects.filter(company_id=OuterRef('cin')).order_by().values('company_id')
    znizenie_imania_issues_count = znizenie_imania_issues_count.annotate(count=Count('*')).values('count')
    data = data.annotate(znizenie_imania_issues_count=Subquery(znizenie_imania_issues_count))

    likvidator_issues_count = LikvidatorIssues.objects.filter(company_id=OuterRef('cin')).order_by().values('company_id')
    likvidator_issues_count = likvidator_issues_count.annotate(count=Count('*')).values('count')
    data = data.annotate(likvidator_issues_count=Subquery(likvidator_issues_count))

    konkurz_vyrovnanie_issues_count = KonkurzVyrovnanieIssues.objects.filter(company_id=OuterRef('cin')).order_by().values('company_id')
    konkurz_vyrovnanie_issues_count = konkurz_vyrovnanie_issues_count.annotate(count=Count('*')).values('count')
    data = data.annotate(konkurz_vyrovnanie_issues_count=Subquery(konkurz_vyrovnanie_issues_count))

    konkurz_restrukturalizacia_actors_count = KonkurzRestrukturalizaciaActors.objects.filter(company_id=OuterRef('cin')).order_by().values('company_id')
    konkurz_restrukturalizacia_actors_count = konkurz_restrukturalizacia_actors_count.annotate(count=Count('*')).values('count')
    data = data.annotate(konkurz_restrukturalizacia_actors_count=Subquery(konkurz_restrukturalizacia_actors_count))
    if params[5] == "asc":
        data = data.order_by(F(params[4]).asc(nulls_last=True))
    else:
        data = data.order_by(F(params[4]).desc(nulls_last=True))
    return data.count(), data[offset:int(params[3]) + offset].values('cin', 'name', 'br_section', 'address_line', 'last_update',
                                                                     'or_podanie_issues_count', 'znizenie_imania_issues_count',
                                                                    'likvidator_issues_count',
                                                                     'konkurz_vyrovnanie_issues_count',
                                                                     'konkurz_restrukturalizacia_actors_count')


def get_companies(request):
    page = request.GET.get("page", "1")
    per_page = request.GET.get("per_page", "10")
    query = request.GET.get("query", '')
    last_update_gte = request.GET.get("last_update_gte", '')
    last_update_lte = request.GET.get("last_update_lte", '')
    order_by = request.GET.get("order_by", 'last_update')
    order_type = request.GET.get("order_type", "desc")
    # params: (last_update_lte, last_update_gte, page, per_page, order_by, order_type)
    params = input_checks.v2_validate_params(last_update_lte, last_update_gte,
                                             page, per_page, order_by, order_type, "companies")
    offset = int(params[3]) * (int(params[2]) - 1)
    count, data = get_comp(query, params, offset)
    metadata = dictmetadata(params[2], params[3], count)
    return {"items": list(data), "metadata": metadata}
