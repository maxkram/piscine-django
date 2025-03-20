from django.shortcuts import render
from .models import People

def display(request):
    """
    Displays characters who are from planets with 'windy' climate.
    """
    records = People.objects.filter(homeworld__climate__icontains='windy') \
                            .order_by('name') \
                            .values_list('name', 'homeworld__name', 'homeworld__climate')
    
    context = {
        'people': list(records),
        'headers': ['Person Name', 'Planet Name', 'Climate']
    }

    if not records.exists():
        context['people'] = []

    return render(request, 'ex09/display.html', context)
