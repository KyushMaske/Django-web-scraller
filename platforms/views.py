from django.shortcuts import render
from django.db.models import Q
from platforms.models import Monumetric, Mediavine, AdThrive

def combined_view(request):
    query = request.GET.get('q', '')
    combined_data = list(Monumetric.objects.all()) + list(Mediavine.objects.all()) + list(AdThrive.objects.all())
    
    if query:
        combined_data = [item for item in combined_data if query.lower() in item.domain.lower()]

    combined_data.sort(key=lambda x: x.date_first_added)

    return render(request, 'platforms/combined.html', {'data': combined_data, 'query': query})
