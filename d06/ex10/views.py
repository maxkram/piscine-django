from django.shortcuts import render
from .forms import CharacterFilterForm
from .models import Movies

def get_filtered_data(data):
    """Filters Movies queryset based on provided criteria and returns values."""
    return Movies.objects.filter(
        characters__gender=data['gender'],
        release_date__gte=data['min_date'],
        release_date__lte=data['max_date'],
        characters__homeworld__diameter__gt=data['diameter']
    ).order_by('release_date').values_list(
        'characters__name',
        'characters__gender',
        'title',
        'characters__homeworld__name',
        'characters__homeworld__diameter'
    )

# Create your views here.
def index(request):
    """Handles form submission and displays results."""
    res = None
    form = CharacterFilterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        res = list(get_filtered_data(form.cleaned_data))

    return render(request, 'ex10/index.html', {'form': form, 'results': res})
