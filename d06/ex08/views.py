# import psycopg2
# from django.shortcuts import render
# from django.http import HttpResponse
    
# import csv
# from io import StringIO

# def init(request):
#     try:
#         conn = psycopg2.connect(
#             dbname="djangotraining",
#             user="djangouser",
#             password="secret",
#             host="localhost"
#         )
#         cur = conn.cursor()

#         # Create ex08_planets table
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS ex08_planets (
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(64) UNIQUE NOT NULL,
#                 climate TEXT,
#                 diameter INT,
#                 orbital_period INT,
#                 population BIGINT,
#                 rotation_period INT,
#                 surface_water REAL,
#                 terrain VARCHAR(128)
#             );
#         """)

#         # Create ex08_people table
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS ex08_people (
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(64) UNIQUE NOT NULL,
#                 birth_year VARCHAR(32),
#                 gender VARCHAR(32),
#                 eye_color VARCHAR(32),
#                 hair_color VARCHAR(32),
#                 height INT,
#                 mass REAL,
#                 homeworld VARCHAR(64) REFERENCES ex08_planets(name)
#             );
#         """)

#         conn.commit()
#         cur.close()
#         conn.close()
#         return HttpResponse("OK")
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")

# def populate(request):
#     try:
#         conn = psycopg2.connect(
#             dbname="djangotraining",
#             user="djangouser",
#             password="secret",
#             host="localhost"
#         )
#         cur = conn.cursor()

#         # Preprocess planets.csv
#         planets_data = StringIO()
#         with open('planets.csv', 'r') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 # Skip the first column (id) and write the rest to StringIO
#                 planets_data.write(','.join(row[1:]) + '\n')
#         planets_data.seek(0)  # Reset the pointer to the beginning of the StringIO object

#         # Use copy_from with the preprocessed data
#         cur.copy_from(planets_data, 'ex08_planets', sep=',', null='',
#                       columns=('name', 'climate', 'diameter', 'orbital_period', 
#                                'population', 'rotation_period', 'surface_water', 'terrain'))

#         # Preprocess people.csv
#         people_data = StringIO()
#         with open('people.csv', 'r') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 # Skip the first column (id) and write the rest to StringIO
#                 people_data.write(','.join(row[1:]) + '\n')
#         people_data.seek(0)  # Reset the pointer to the beginning of the StringIO object

#         # Use copy_from with the preprocessed data
#         cur.copy_from(people_data, 'ex08_people', sep=',', null='',
#                       columns=('name', 'birth_year', 'gender', 'eye_color', 
#                                'hair_color', 'height', 'mass', 'homeworld'))

#         conn.commit()
#         cur.close()
#         conn.close()
#         return HttpResponse("OK")
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")
    
# def display(request):
#     try:
#         conn = psycopg2.connect(
#             dbname="djangotraining",
#             user="djangouser",
#             password="secret",
#             host="localhost"
#         )
#         cur = conn.cursor()

#         # Query to get the required data
#         cur.execute("""
#             SELECT p.name, p.homeworld, pl.climate
#             FROM ex08_people p
#             JOIN ex08_planets pl ON p.homeworld = pl.name
#             WHERE pl.climate LIKE '%windy%' OR pl.climate LIKE '%moderately windy%'
#             ORDER BY p.name ASC;
#         """)

#         rows = cur.fetchall()
#         cur.close()
#         conn.close()

#         if not rows:
#             return HttpResponse("No data available")

#         # Render the data in an HTML table
#         html = "<table><tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
#         for row in rows:
#             html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
#         html += "</table>"

#         return HttpResponse(html)
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}")

from django.shortcuts import render
import psycopg2
from django.db import connection 
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

def connect_execute(sql: str):
    db = settings.DATABASES.default
    try:
        conn = psycopg2.connect(
            database=db['NAME'],
            user=db['USER'],
            password=db['PASSWORD'],
            host=db['HOST'],
            port=db['PORT'],
        )
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
        conn.close()
    except psycopg2.Error as e:
        conn.close()
        raise e

def execute(sql: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            cursor.execute('commit')
    except Exception as e:
        raise e

# Create your views here.
def init(request):
    message = 'OK'
    try:
        # Drop tables if they exist
        execute('DROP TABLE IF EXISTS ex08_people;')
        execute('DROP TABLE IF EXISTS ex08_planets;')

        # Create ex08_planets table
        execute('''CREATE TABLE ex08_planets (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR(64),
            diameter INT,
            orbital_period INT,
            population BIGINT,
            rotation_period INT,
            surface_water REAL,
            terrain VARCHAR(128)
        );''')

        # Create ex08_people table
        execute('''CREATE TABLE ex08_people (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height INT,
            mass REAL,
            homeworld VARCHAR(64),
            FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
        );''')
    except Exception as e:
        message = f'Error: {e}'
    return HttpResponse(message)

def populate(request):
    message = ''
    try:
        with connection.cursor() as cursor:
            with open('./assets/planets.csv') as f:
                cursor.copy_from(f, 'ex08_planets', sep='\t', null='NULL', columns=['name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain'])
                message += f'planets.csv OK<br/>'
            with open('./assets/people.csv') as f:
                cursor.copy_from(f, 'ex08_people', sep='\t', null='NULL', columns=['name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld'])
                message += f'people.csv OK<br/>'
    except Exception as e:
        message =  f'Error: {e}'
    return HttpResponse(message)

def display(request):
    context = {'people' : [], 'headers' : ['Person Name', 'Planet Name', 'Climate']}
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT pe.name, pl.name, pl.climate 
                           FROM ex08_people AS pe 
                           JOIN ex08_planets AS pl
                           ON pe.homeworld = pl.name
                           WHERE pl.climate LIKE '%windy%'
                           ORDER BY pe.name ASC;""")
            records = cursor.fetchall()
        if len(records) == 0:
            raise Exception()
        context['people'] = records
    except Exception as e:
        print(e)
        context['people'] = []
    return render(request, 'ex08/display.html', context)