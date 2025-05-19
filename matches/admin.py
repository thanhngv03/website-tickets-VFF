from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'ticket_price')
    search_fields = ('title', 'location')
    list_filter = ('date',)
