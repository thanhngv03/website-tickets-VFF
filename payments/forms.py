from django import forms
from payments.models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method']
        widgets = {
            'method': forms.Select(attrs={'class': 'border p-2 rounded-lg w-full'}),
        }
        labels = {
            'method': 'Phương thức thanh toán',
        }
