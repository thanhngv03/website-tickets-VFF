from django.urls import path
from . import views

app_name = 'payments' 

urlpatterns = [
    path('checkout/<int:ticket_id>/', views.payment_checkout, name='checkout'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
]
