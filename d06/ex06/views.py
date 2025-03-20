import psycopg2
from django.http import HttpResponse
from django.shortcuts import render  # Import render

# Database connection helper function
def get_db_connection():
    return psycopg2.connect(
        dbname="djangotraining",
        user="djangouser",
        password="secret",
        host="localhost",
        port="5432"
    )

# View for /ex06/init (unchanged)
def init(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM pg_tables 
                WHERE schemaname = 'public' AND tablename = 'ex06_movies'
            );
        """)
        table_exists = cur.fetchone()[0]
        if table_exists:
            cur.execute("DROP TABLE ex06_movies CASCADE;")
            conn.commit()
        cur.execute("""
            CREATE TABLE ex06_movies (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INTEGER PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE OR REPLACE FUNCTION update_timestamp()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        cur.execute("""
            DROP TRIGGER IF EXISTS update_ex06_movies_timestamp ON ex06_movies;
            CREATE TRIGGER update_ex06_movies_timestamp
            BEFORE UPDATE ON ex06_movies
            FOR EACH ROW EXECUTE FUNCTION update_timestamp();
        """)
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

# View for /ex06/populate (unchanged)
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
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for episode_nb, title, director, producer, release_date in movies:
            try:
                cur.execute("""
                    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (episode_nb) DO NOTHING;
                """, (episode_nb, title, director, producer, release_date))
                results.append("OK")
            except Exception as e:
                results.append(f"Error inserting {title}: {str(e)}")
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

# View for /ex06/display (unchanged)
def display(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ex06_movies ORDER BY episode_nb;")
        rows = cur.fetchall()
        if not rows:
            return HttpResponse("No data available")
        table = "<table border='1'><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th><th>Created</th><th>Updated</th></tr>"
        for row in rows:
            table += "<tr>"
            for col in row:
                table += f"<td>{col if col is not None else ''}</td>"
            table += "</tr>"
        table += "</table>"
        cur.close()
        conn.close()
        return HttpResponse(table)
    except Exception as e:
        return HttpResponse("No data available")

# Updated View for /ex06/update
def update(request):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Handle POST request
        if request.method == "POST":
            title = request.POST.get("title")
            opening_crawl = request.POST.get("opening_crawl")
            if title and opening_crawl:
                cur.execute("""
                    UPDATE ex06_movies
                    SET opening_crawl = %s
                    WHERE title = %s;
                """, (opening_crawl, title))
                conn.commit()
        
        # Fetch titles for the dropdown
        cur.execute("SELECT title FROM ex06_movies ORDER BY title;")
        titles = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        if not titles:
            return HttpResponse("No data available")
        
        # Render the template with titles
        return render(request, 'ex06/update.html', {'titles': titles})
    except Exception as e:
        return HttpResponse("No data available")