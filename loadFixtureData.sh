#!/bin/sh
python manage.py loaddata fixture infoworks/fixtures/initial_config_data.json
python manage.py loaddata fixture infoworks/fixtures/initial_systemcode.json
python manage.py loaddata fixture infoworks/fixtures/initial_lookuptable.json 
python manage.py loaddata fixture infoworks/fixtures/initial_lookuptableelement.json
python manage.py loaddata fixture infoworks/fixtures/initial_dimensionname.json
python manage.py loaddata fixture infoworks/fixtures/initial_dimensionfor.json
python manage.py loaddata fixture infoworks/fixtures/initial_customdimensionyname.json
