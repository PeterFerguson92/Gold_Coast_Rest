Steps
--- Database Set Up ---
1 - Install PostgresSQL
2 - From the terminal enter into PostgresSQL command line (type psql)
3 - Create Database - CREATE DATABASE gold_coast_bookings;
4 - Create Role - CREATE ROLE django_gold_coast_bookings WITH LOGIN PASSWORD 'goldcoast';
5 - GRANT ALL PRIVILEGES ON DATABASE gold_coast_bookings TO django_gold_coast_bookings;

--- Project Set Up ---
6 - Activate VirtualEnviroment - source goldCoastVenv/bin/activate
7 - Install Dependecies - pip install -r requirements.txt
8 - Run Project - python manage.py runserver
