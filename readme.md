python -m venv entorno
source entorno/bin/activate

pip install django
django-admin startproject EsportsHubMain
python manage.py runserver
python manage.py startapp EsportHub

pip install django requests


Iniciar proyecto:
1. source entorno/bin/activate
2. cd EsportsHubMain
3. python manage.py runserver


Ruta para crons:
* * * * * cd /Users/facuhansen/Desktop/EsportsHubWorkSpace && source entorno/bin/activate && cd /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain && /Users/facuhansen/Desktop/EsportsHubWorkSpace/entorno/bin/python /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain/manage.py runcrons > /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain/log/runcrons.log

Ruta para crons pero sin el source;

* * * * * cd /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain && /Users/facuhansen/Desktop/EsportsHubWorkSpace/entorno/bin/python anage.py runcrons > /Users/facuhansen/Desktop/EsportsHubWorkSpace/EsportsHubMain/log/runcrons.log 2>&1


/entorno/
/EsportsHubMain/
--EsportsHub/
----__pycache__.py
----management/
----migrations/
----templates/
------registration/
--------login.html
--------password_reset_complete.html
--------password_reset_confirm.html
--------password_reset_done.html
--------password_reset_email.html
--------password_reset_form.html
--------register.html
------404.html
------base.html
------index.html
------match_detail.html
------matches_now.html
------matches_today.html
------profile.html
------search_results.html
------team_detail.html
------team_matches.html
------team_list.html
------tournament_detail.html
------tournaments_list.html
------update_profile.html
----admin.py
----apps.py
----forms.py
----models.py
----test.py
----views.py
--EsportsHubMain/
----asgi.py
----settings.py
----urls..py
----wsgi.py
--manage.py
--db.sqlite3

