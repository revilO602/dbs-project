## Aplikačný server pre databázu

### Oliver Leontiev

### FIIT STU, projekt na predmet DBS

ID commitu pre zadanie 5: v súbore *commit_id.txt* (iba v AISe)

#### Prístup

Adresa aplikačného servera :  https://fiit-dbs-xleontiev-app.azurewebsites.net

#### Implementácia

Implementácia je v pythone pomocou modulu Django. Samotné query sú vytvárané v *raw_query_builder.py* a validacia parametrov pre query prebieha v *input_checks.py*.

Implementácia cez ORM je v triedach s "v2" v názve.

Potrebné moduly pre beh programu sú v súbore *requirements.txt*.