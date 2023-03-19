SUBMISSIONS_COLUMNS = ("p.id, p.br_court_name, p.kind_name, p.cin, p.registration_date, " +
           "p.corporate_body_name, p.br_section, p.br_insertion, p.text, p.street, " +
           "p.postal_code, p.city")

# query template for the GET request
def submissions_getquery(order_by, order_type, date_lte, date_gte):
    rawSQL = ("PREPARE searchQuery (text, int, int, int) as " +
              "SELECT " + SUBMISSIONS_COLUMNS + " from ov.or_podanie_issues as p " +
              "where ((concat(corporate_body_name, ' ', city) ilike $1) " +
              "or (cin = $2)) ")
    if date_lte:
        rawSQL = rawSQL + "and (registration_date <= '" + date_lte + "') "
    if date_gte:
        rawSQL = rawSQL + "and (registration_date >= '" + date_gte + "') "
    rawSQL = rawSQL + ("order by p." + order_by + " " + order_type + " OFFSET $3 LIMIT $4; " +
             "EXECUTE searchQuery(%s, %s, %s, %s);")
    return rawSQL

# query to get metadata for GET request
def submissions_gettotalquery(date_lte, date_gte):
    rawSQL = ("PREPARE countQuery (text, int) as " +
              "SELECT count(*) from ov.or_podanie_issues as p " +
              "where ((concat(corporate_body_name, ' ', city) ilike $1) " +
              "or (cin = $2)) ")
    if date_lte:
        rawSQL = rawSQL + "and (registration_date <= '" + date_lte + "') "
    if date_gte:
        rawSQL = rawSQL + "and (registration_date >= '" + date_gte + "') "
    rawSQL = rawSQL + "; EXECUTE countQuery(%s, %s);"
    return rawSQL

# query to insert new row into bulletin_issues
def submissions_insert_bulletin_query():
    rawSQL = ("insert into ov.bulletin_issues(number, year, published_at, created_at, updated_at)" +
              "select max(b.number) + 1, date_part('year', now()), now(), now(), now()" +
              "from ov.bulletin_issues as b where year = date_part('year', now())" +
              "returning(id);")
    return rawSQL


# query to insert new row into raw_issues
def submissions_insert_raw_query():
    rawSQL = ("insert into ov.raw_issues(bulletin_issue_id, file_name, content, created_at, updated_at)" +
              "values(%s, '-', '-', now(), now())" +
              "returning(id);")
    return rawSQL

# query to insert new row into podanie_issues
def submissions_insert_podanie_query():
    rawSQL = ("PREPARE insertPodanie(int, int, text, text, int, date, text, text, " +
              "text, text, text, text, text) as " +
              "INSERT into ov.or_podanie_issues (bulletin_issue_id, raw_issue_id, br_mark, " +
              "br_court_code, br_court_name, kind_code, " +
              "kind_name, cin, registration_date, corporate_body_name, " +
              "br_section, br_insertion, text, created_at, updated_at, " +
              "address_line, street, postal_code, city) " +
              "VALUES ($1, $2, '-', '-', $3, '-', $4, $5, " +
              "$6, $7, $8, $9, $10, now(), " +
              "now(), $11, $12, $13, $14) " +
              "RETURNING id, br_court_name, kind_name, cin, registration_date, corporate_body_name, " +
              "br_section, br_insertion, text, street, postal_code, city; " +
              "EXECUTE insertPodanie(%s, %s, %s, %s, %s, %s, %s, " +
              "%s, %s, %s, %s, %s, %s, %s);")
    return rawSQL

def submissions_delete_query():
    rawSQL = ("delete from ov.or_podanie_issues where id=%s RETURNING id;")
    return rawSQL

def companies_get_query(order_by, order_type, date_lte, date_gte):
    rawSQL = ("""PREPARE searchCompanies (varchar, int, int) as
    select com.cin, com.name, com.br_section, com.address_line, com.last_update,
	   or_podanie_issues_count, znizenie_imania_issues_count,  likvidator_issues_count, 
       konkurz_vyrovnanie_issues_count, konkurz_restrukturalizacia_actors_count
    from (select cin, name, br_section, address_line, last_update from ov.companies
    ) com
    left join
    (select company_id, count(*) or_podanie_issues_count from ov.or_podanie_issues
    where company_id is not null
    group by company_id) opi
    on (com.cin = opi.company_id)
    left join
    (select company_id, count(*) likvidator_issues_count from ov.likvidator_issues
    where company_id is not null
    group by company_id) li
    on (com.cin = li.company_id)
    left join
    (select company_id, count(*) konkurz_vyrovnanie_issues_count from ov.konkurz_vyrovnanie_issues
    where company_id is not null
    group by company_id) kvi
    on (com.cin = kvi.company_id)
    left join
    (select company_id, count(*) znizenie_imania_issues_count from ov.znizenie_imania_issues
    where company_id is not null
    group by company_id) zii
    on (com.cin = zii.company_id)
    left join
    (select company_id, count(*) konkurz_restrukturalizacia_actors_count from ov.konkurz_restrukturalizacia_actors
    where company_id is not null
    group by company_id) kra
    on (com.cin = kra.company_id)
    where (concat(com.name, ' ', com.address_line) ilike $1)""")
    if date_lte:
        rawSQL = rawSQL + " and (last_update <= '" + date_lte + "')"
    if date_gte:
        rawSQL = rawSQL + " and (last_update >= '" + date_gte + "')"
    rawSQL = rawSQL + ("order by " + order_by + " " + order_type + " OFFSET $2 LIMIT $3; " +
    "EXECUTE searchCompanies(%s, %s, %s);")
    return rawSQL

def companies_get_totalquery(date_lte, date_gte):
    rawSQL = ("""PREPARE countCompanies (varchar) as
        select count(*)
        from ov.companies as com
        where (concat(com.name, ' ', com.address_line) ilike $1)""")
    if date_lte:
        rawSQL = rawSQL + "and (last_update <= '" + date_lte + "') "
    if date_gte:
        rawSQL = rawSQL + "and (last_update >= '" + date_gte + "') "
    rawSQL = rawSQL + "; EXECUTE countCompanies(%s);"
    return rawSQL