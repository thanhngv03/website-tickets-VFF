from django.shortcuts import render, get_object_or_404, redirect
from tickets.models import Ticket
from .models import Payment
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required

@login_required
def payment_checkout(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if Payment.objects.filter(ticket=ticket).exists():
        payment = Payment.objects.get(ticket=ticket)
        return redirect('payments:payment_success', payment_id=payment.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.ticket = ticket
            payment.amount = ticket.price()
            payment.status = 'success'  # mô phỏng thành công
            payment.save()
            return redirect('payments:payment_success', payment_id=payment.id)
    else:
        form = PaymentForm()

    return render(request, 'payments/checkout.html', {'form': form, 'ticket': ticket})


@login_required
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payments/success.html', {'payment': payment})
