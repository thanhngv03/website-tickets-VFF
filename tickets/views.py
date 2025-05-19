from django.shortcuts import render, redirect, get_object_or_404
from matches.models import Match
from .models import Seat, Ticket
from django.contrib.auth.decorators import login_required

@login_required
def choose_seat(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    seats = Seat.objects.filter(match=match)
    if request.method == "POST":
        seat_id = request.POST.get("seat_id")
        seat = get_object_or_404(Seat, id=seat_id, is_booked=False)
        seat.is_booked = True
        seat.save()
        Ticket.objects.create(user=request.user, match=match, seat=seat)
        return redirect("ticket_success")
    return render(request, "tickets/choose_seat.html", {"match": match, "seats": seats})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).select_related('match', 'seat')
    return render(request, "tickets/my_tickets.html", {'tickets': tickets})

def ticket_success(request):
    return render(request, "tickets/success.html")
