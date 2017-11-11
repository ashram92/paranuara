#!/bin/bash -e

USER=root;
DB=paranuara

echo "Deleting database...";
mysql -u $USER -p -e "DROP DATABASE $DB;";

echo "Creating database...";
mysql -u $USER -p -e "CREATE DATABASE $DB;";

virtualenv ENV;
source ENV/bin/activate;

pip install -r requirements.txt;

python manage.py migrate;
python manage.py import_companies resources/companies.json;
python manage.py import_people resources/people.json;
