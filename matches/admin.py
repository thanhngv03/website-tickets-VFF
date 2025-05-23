from django.contrib import admin
from .models import Match
from django.contrib.admin import AdminSite



admin.site.site_header = "Quản trị bán vé VFF"
admin.site.site_title = "VFF Ticket Admin"
admin.site.index_title = "Trang quản lý hệ thống vé"
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display =  ('title', 'date', 'start_time', 'is_open_for_sale')
    search_fields = ('title', 'location')
    list_filter = ('date',)
