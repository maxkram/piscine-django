from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Movies

def populate(request):
    movies_data = [
        {
            "episode_nb": 1,
            "title": "The Phantom Menace",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "episode_nb": 2,
            "title": "Attack of the Clones",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16",
        },
        {
            "episode_nb": 3,
            "title": "Revenge of the Sith",
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19",
        },
        {
            "episode_nb": 4,
            "title": "A New Hope",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
        },
        {
            "episode_nb": 5,
            "title": "The Empire Strikes Back",
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17",
        },
        {
            "episode_nb": 6,
            "title": "Return of the Jedi",
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
        },
        {
            "episode_nb": 7,
            "title": "The Force Awakens",
            "director": "J.J. Abrams",
            "producer": "Kathleen Kennedy, J.J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]
    results = []
    for movie in movies_data:
        try:
            Movies.objects.create(**movie)
            results.append(f"OK: {movie['title']}")
        except IntegrityError as e:
            results.append(f"Error: {movie['title']} - {e}")
    return HttpResponse("<br>".join(results))

def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")
        return render(request, 'ex07/display.html', {'movies': movies})
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    
def update(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            opening_crawl = request.POST.get('opening_crawl')
            movie = Movies.objects.get(title=title)
            movie.opening_crawl = opening_crawl
            movie.save()
            return redirect('/ex07/update')

        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")
        return render(request, 'ex07/update.html', {'movies': movies})
    except Exception as e:
        return HttpResponse(f"Error: {e}")