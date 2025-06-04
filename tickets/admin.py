from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Seat, Ticket
from matches.models import Match

# Nhập match, khán đài, số lượng ghế
class SeatBulkCreateForm(forms.Form):
    match = forms.ModelChoiceField(queryset=Match.objects.all(), label="Trận đấu")
    seat_number = forms.ChoiceField(choices=Seat.SEAT_CHOICES, label="Khán đài")
    quantity = forms.IntegerField(min_value=1, label="Số lượng ghế")

# Admin tùy chỉnh
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('match', 'seat_number', 'code', 'is_booked')
    list_filter = ('match', 'seat_number', 'is_booked')
    search_fields = ('code',)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-add/', self.admin_site.admin_view(self.bulk_add_view), name='seat_bulk_add'),
        ]
        return custom_urls + urls

    def bulk_add_view(self, request):
        if request.method == 'POST':
            form = SeatBulkCreateForm(request.POST)
            if form.is_valid():
                match = form.cleaned_data['match']
                seat_number = form.cleaned_data['seat_number']
                quantity = form.cleaned_data['quantity']

                created = 0
                for i in range(1, quantity + 1):
                    code = f"{seat_number}-{i:03d}"
                    if not Seat.objects.filter(match=match, code=code).exists():
                        Seat.objects.create(match=match, seat_number=seat_number, code=code)
                        created += 1

                messages.success(request, f"✅ Đã tạo {created} ghế cho {match.title} tại khán đài {seat_number}")
                return redirect('..')
        else:
            form = SeatBulkCreateForm()

        return render(request, 'admin/seat_bulk_form.html', {'form': form})

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'seat', 'booked_at')
    list_filter = ('match', 'booked_at')
    search_fields = ('user__username', 'match__title', 'seat__code')
