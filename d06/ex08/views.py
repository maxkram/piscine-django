from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
import csv

def init(request):
    try:
        with connection.cursor() as cursor:
            # Drop tables if they exist
            cursor.execute("DROP TABLE IF EXISTS ex08_people;")
            cursor.execute("DROP TABLE IF EXISTS ex08_planets;")
            
            # Create the ex08_planets table
            cursor.execute("""
                CREATE TABLE ex08_planets (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    climate VARCHAR(128),
                    diameter INTEGER,
                    orbital_period INTEGER,
                    population BIGINT,
                    rotation_period INTEGER,
                    surface_water REAL,
                    terrain VARCHAR(128)
                );
            """)
            
            # Create the ex08_people table
            cursor.execute("""
                CREATE TABLE ex08_people (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    birth_year VARCHAR(32),
                    gender VARCHAR(32),
                    eye_color VARCHAR(32),
                    hair_color VARCHAR(32),
                    height INTEGER,
                    mass REAL,
                    homeworld VARCHAR(64),
                    CONSTRAINT fk_homeworld FOREIGN KEY (homeworld)
                        REFERENCES ex08_planets(name)
                        ON DELETE CASCADE
                );
            """)
        
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    try:
        results = []
        
        # Populate ex08_planets
        with open('planets.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            with connection.cursor() as cursor:
                for row in reader:
                    try:
                        cursor.execute("""
                            INSERT INTO ex08_planets (
                                name, climate, diameter, orbital_period, population,
                                rotation_period, surface_water, terrain
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """, row)
                        results.append(f"OK: Planet {row[0]}")
                    except Exception as e:
                        results.append(f"Error: Planet {row[0]} - {e}")
        
        # Populate ex08_people
        with open('people.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            with connection.cursor() as cursor:
                for row in reader:
                    try:
                        cursor.execute("""
                            INSERT INTO ex08_people (
                                name, birth_year, gender, eye_color, hair_color,
                                height, mass, homeworld
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """, row)
                        results.append(f"OK: Person {row[0]}")
                    except Exception as e:
                        results.append(f"Error: Person {row[0]} - {e}")
        
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def display(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.name AS person_name, pl.name AS planet_name, pl.climate
                FROM ex08_people p
                JOIN ex08_planets pl ON p.homeworld = pl.name
                WHERE pl.climate ILIKE '%windy%'
                ORDER BY p.name ASC;
            """)
            data = cursor.fetchall()
            if not data:
                return HttpResponse("No data available")
        return render(request, 'ex08/display.html', {'data': data})
    except Exception as e:
        return HttpResponse(f"Error: {e}")