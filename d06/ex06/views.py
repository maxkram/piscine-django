from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse

def init(request):
    try:
        with connection.cursor() as cursor:
            # Create the table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex06_movies (
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) UNIQUE NOT NULL,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL,
                    created TIMESTAMP DEFAULT NOW(),
                    updated TIMESTAMP DEFAULT NOW()
                );
            """)
            # Create the trigger
            cursor.execute("""
                CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated = NOW();
                    NEW.created = OLD.created;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)
            cursor.execute("""
                CREATE TRIGGER update_films_changetimestamp
                BEFORE UPDATE ON ex06_movies
                FOR EACH ROW
                EXECUTE PROCEDURE update_changetimestamp_column();
            """)
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
def populate(request):
    movies = [
        (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
        (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
        (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11"),
    ]
    results = []
    for episode_nb, title, director, producer, release_date in movies:
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (episode_nb) DO NOTHING;
                """, [episode_nb, title, director, producer, release_date])
            results.append("OK")
        except Exception as e:
            results.append(f"Error: {str(e)}")
    return HttpResponse("<br>".join(results))

def display(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ex06_movies")
            movies = cursor.fetchall()
        if not movies:
            return HttpResponse("No data available")
        html = "<table border='1'><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th><th>Created</th><th>Updated</th></tr>"
        for movie in movies:
            html += f"<tr><td>{movie[1]}</td><td>{movie[0]}</td><td>{movie[2] or ''}</td><td>{movie[3]}</td><td>{movie[4]}</td><td>{movie[5]}</td><td>{movie[6]}</td><td>{movie[7]}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
def update(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            opening_crawl = request.POST.get('opening_crawl')
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ex06_movies
                    SET opening_crawl = %s
                    WHERE title = %s;
                """, [opening_crawl, title])
            return HttpResponse("OK")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT title FROM ex06_movies")
            movies = cursor.fetchall()
        if not movies:
            return HttpResponse("No data available")
        return render(request, 'ex06/update.html', {'movies': movies})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")