from django.shortcuts import render
from django.http import HttpResponse
from .models import Movies
from datetime import datetime

# View for /ex07/populate
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
        # Delete all existing records in the Movies table
        Movies.objects.all().delete()
        
        # Insert the new records
        for episode_nb, title, director, producer, release_date in movies:
            try:
                Movies.objects.create(
                    episode_nb=episode_nb,
                    title=title,
                    director=director,
                    producer=producer,
                    release_date=datetime.strptime(release_date, "%Y-%m-%d").date()
                )
                results.append("OK")
            except Exception as e:
                results.append(f"Error inserting {title}: {str(e)}")
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

# View for /ex07/display
def display(request):
    try:
        movies = Movies.objects.all().order_by('episode_nb')
        if not movies:
            return HttpResponse("No data available")
        return render(request, 'ex07/display.html', {'movies': movies})
    except Exception as e:
        return HttpResponse("No data available")

# View for /ex07/update
def update(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title")
            opening_crawl = request.POST.get("opening_crawl")
            if title and opening_crawl:
                movie = Movies.objects.get(title=title)
                movie.opening_crawl = opening_crawl
                movie.save()
        
        movies = Movies.objects.all().order_by('title')
        if not movies:
            return HttpResponse("No data available")
        return render(request, 'ex07/update.html', {'movies': movies})
    except Exception as e:
        return HttpResponse("No data available")