from django.http import HttpResponse
from .models import Movies
from django.utils.dateparse import parse_date

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
            Movies.objects.get_or_create(
                episode_nb=episode_nb,
                defaults={
                    'title': title,
                    'director': director,
                    'producer': producer,
                    'release_date': parse_date(release_date),
                }
            )
            results.append("OK")
        except Exception as e:
            results.append(f"Error: {str(e)}")
    return HttpResponse("<br>".join(results))

def display(request):
    movies = Movies.objects.all()
    if not movies:
        return HttpResponse("No data available")
    html = "<table border='1'><tr><th>Title</th><th>Episode</th><th>Opening Crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
    for movie in movies:
        html += f"<tr><td>{movie.title}</td><td>{movie.episode_nb}</td><td>{movie.opening_crawl or ''}</td><td>{movie.director}</td><td>{movie.producer}</td><td>{movie.release_date}</td></tr>"
    html += "</table>"
    return HttpResponse(html)