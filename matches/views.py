from django.http import JsonResponse
from .models import Match
from datetime import datetime
from django.shortcuts import render


def home(request):
    matches = Match.objects.all().order_by('date')
    return render(request, "home.html", {"matches": matches})


def filter_matches(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except Exception as e:
        return JsonResponse({'error': 'Ngày không hợp lệ'}, status=400)

    matches = Match.objects.filter(date__range=(start_date, end_date)).order_by('date')
    match_list = [{
        'title': m.title,
        'date': m.date.strftime("%d/%m/%Y"),
        'location': m.location
    } for m in matches]

    return JsonResponse({'results': match_list})
