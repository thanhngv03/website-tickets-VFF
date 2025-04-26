from django.contrib import admin
from .models import Seat, Ticket # Lỗi Error

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('match', 'seat_number', 'is_booked')
    list_filter = ('match', 'is_booked')
    search_fields = ('seat_number',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'seat', 'booked_at')
    list_filter = ('match', 'booked_at')
