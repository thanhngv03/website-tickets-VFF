from django.urls import path
from . import views

urlpatterns = [
    path("book/<int:match_id>/", views.choose_seat, name="choose_seat"),
    path("success/", views.ticket_success, name="ticket_success"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),

]
