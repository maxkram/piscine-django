from django.http import HttpResponse
import psycopg2
from psycopg2 import Error

def init(request):
    try:
        conn = psycopg2.connect(dbname="djangotraining", user="djangouser", password="secret", host="localhost")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ex02_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        """)
        conn.commit()
        return HttpResponse("OK")
    except Error as e:
        return HttpResponse(f"Error: {str(e)}")
    finally:
        cur.close()
        conn.close()

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
    try:
        conn = psycopg2.connect(dbname="djangotraining", user="djangouser", password="secret", host="localhost")
        cur = conn.cursor()
        results = []
        for episode_nb, title, director, producer, release_date in movies:
            try:
                cur.execute("""
                    INSERT INTO ex02_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (episode_nb, title, director, producer, release_date))
                results.append("OK")
            except Error as e:
                results.append(f"Error: {str(e)}")
        conn.commit()
        return HttpResponse("<br>".join(results))
    except Error as e:
        return HttpResponse(f"Error: {str(e)}")
    finally:
        cur.close()
        conn.close()

def display(request):
    try:
        conn = psycopg2.connect(dbname="djangotraining", user="djangouser", password="secret", host="localhost")
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex02_movies;")
        rows = cur.fetchall()
        if not rows:
            return HttpResponse("No data available")
        html = "<table border='1'><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2] or ''}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Error as e:
        return HttpResponse("No data available")
    finally:
        cur.close()
        conn.close()