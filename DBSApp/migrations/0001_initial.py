# Generated by Django 3.1.7 on 2021-03-25 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("""Create Table ov.companies(
cin bigint primary key,
name varchar,
br_section varchar,
last_update timestamp without time zone,
address_line varchar,
created_at timestamp without time zone,
updated_at timestamp without time zone
);
--
INSERT INTO ov.companies (cin, name, br_section, last_update, address_line,
						 created_at, updated_at)
SELECT cin, corporate_body_name, br_section, updated_at, address_line, now(), now()
FROM (
    SELECT t.cin, t.corporate_body_name, t.br_section, 
	t.updated_at, t.address_line, 
	row_number() 
	OVER (PARTITION BY t.cin ORDER BY t.updated_at desc) rn
    FROM ov.or_podanie_issues as t
    WHERE t.cin is not null
) p
WHERE rn = 1 ORDER BY p.updated_at desc
on conflict do nothing;

ALTER TABLE ov.or_podanie_issues
ADD COLUMN company_id bigint;

UPDATE ov.or_podanie_issues
SET company_id = cin;
-- 
INSERT INTO ov.companies (cin, name, br_section, last_update, address_line,
						 created_at, updated_at)
SELECT cin, corporate_body_name, br_section, updated_at, address_line, now(), now()
FROM (
    SELECT t.cin, t.corporate_body_name, t.br_section, 
	t.updated_at, concat(t.street,', ',t.postal_code, ' ', t.city) as address_line, 
	row_number() 
	OVER (PARTITION BY t.cin ORDER BY t.updated_at desc) rn
    FROM ov.likvidator_issues as t
    WHERE t.cin is not null
) p
WHERE rn = 1 ORDER BY p.updated_at desc
on conflict do nothing;

ALTER TABLE ov.likvidator_issues
ADD COLUMN company_id bigint;

UPDATE ov.likvidator_issues
SET company_id = cin;
--
INSERT INTO ov.companies (cin, name, br_section, last_update, address_line,
						 created_at, updated_at)
SELECT cin, corporate_body_name, null, updated_at, address_line, now(), now()
FROM (
    SELECT t.cin, t.corporate_body_name, 
	t.updated_at, concat(t.street,', ',t.postal_code, ' ', t.city) as address_line, 
	row_number() 
	OVER (PARTITION BY t.cin ORDER BY t.updated_at desc) rn
    FROM ov.konkurz_vyrovnanie_issues as t
    WHERE t.cin is not null
) p
WHERE rn = 1 ORDER BY p.updated_at desc
on conflict do nothing;

ALTER TABLE ov.konkurz_vyrovnanie_issues
ADD COLUMN company_id bigint;

UPDATE ov.konkurz_vyrovnanie_issues
SET company_id = cin;
--
INSERT INTO ov.companies (cin, name, br_section, last_update, address_line,
						 created_at, updated_at)
SELECT cin, corporate_body_name, br_section, updated_at, address_line, now(), now()
FROM (
    SELECT t.cin, t.corporate_body_name, t.br_section, 
	t.updated_at, concat(t.street,', ',t.postal_code, ' ', t.city) as address_line, 
	row_number() 
	OVER (PARTITION BY t.cin ORDER BY t.updated_at desc) rn
    FROM ov.znizenie_imania_issues as t
    WHERE t.cin is not null
) p
WHERE rn = 1 ORDER BY p.updated_at desc
on conflict do nothing;

ALTER TABLE ov.znizenie_imania_issues
ADD COLUMN company_id bigint;

UPDATE ov.znizenie_imania_issues
SET company_id = cin;
--
INSERT INTO ov.companies (cin, name, br_section, last_update, address_line,
						 created_at, updated_at)
SELECT cin, corporate_body_name, null, updated_at, address_line, now(), now()
FROM (
    SELECT t.cin, t.corporate_body_name, 
	t.updated_at, concat(t.street,', ',t.postal_code, ' ', t.city) as address_line, 
	row_number() 
	OVER (PARTITION BY t.cin ORDER BY t.updated_at desc) rn
    FROM ov.konkurz_restrukturalizacia_actors as t
    WHERE t.cin is not null
) p
WHERE rn = 1 ORDER BY p.updated_at desc
on conflict do nothing;

ALTER TABLE ov.konkurz_restrukturalizacia_actors
ADD COLUMN company_id bigint;

UPDATE ov.konkurz_restrukturalizacia_actors
SET company_id = cin;

ALTER TABLE ov.or_podanie_issues
ADD CONSTRAINT cinfk
	FOREIGN KEY (company_id)
	REFERENCES ov.companies(cin);

ALTER TABLE ov.likvidator_issues
ADD CONSTRAINT cinfk
	FOREIGN KEY (company_id)
	REFERENCES ov.companies(cin);
	
ALTER TABLE ov.znizenie_imania_issues
ADD CONSTRAINT cinfk
	FOREIGN KEY (company_id)
	REFERENCES ov.companies(cin);
	
ALTER TABLE ov.konkurz_restrukturalizacia_actors
ADD CONSTRAINT cinfk
	FOREIGN KEY (company_id)
	REFERENCES ov.companies(cin);

ALTER TABLE ov.konkurz_vyrovnanie_issues
ADD CONSTRAINT cinfk
	FOREIGN KEY (company_id)
	REFERENCES ov.companies(cin);
	
CREATE INDEX ON ov.or_podanie_issues (company_id);
CREATE INDEX ON ov.likvidator_issues (company_id);
CREATE INDEX ON ov.konkurz_vyrovnanie_issues (company_id);
CREATE INDEX ON ov.znizenie_imania_issues (company_id);
CREATE INDEX ON ov.konkurz_restrukturalizacia_actors (company_id);""")
    ]
