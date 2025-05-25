from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from matches.models import Match
from .models import Seat, Ticket
from collections import defaultdict
from django.shortcuts import render

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).select_related("seat", "match")
    return render(request, "tickets/my_tickets.html", {"tickets": tickets})

def ticket_success(request):
    return render(request, "tickets/success.html")

@login_required
def choose_seat(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    seats = Seat.objects.filter(match=match)

    if request.method == "POST":
        seat_id = request.POST.get("seat_id")
        seat = get_object_or_404(Seat, id=seat_id, is_booked=False)
        seat.is_booked = True
        seat.save()

        # ✅ Gán vào biến ticket để lấy ID
        ticket = Ticket.objects.create(user=request.user, match=match, seat=seat)

        return redirect("payments:checkout", ticket_id=ticket.id)

    # Nhóm ghế theo khán đài
    seat_sections = sorted(set(seats.values_list('seat_number', flat=True)))
    from collections import defaultdict
    seats_by_section = defaultdict(list)
    for seat in seats:
        seats_by_section[seat.seat_number].append(seat)

    return render(request, "tickets/choose_seat.html", {
        "match": match,
        "seat_sections": seat_sections,
        "seats_by_section": seats_by_section,
    })
