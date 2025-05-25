from django.db import models
from django.contrib.auth.models import User
from tickets.models import Ticket

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('momo', 'Momo'),
        ('vnpay', 'VNPay'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('cash', 'Tiền mặt'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Đang xử lý'),
        ('success', 'Thành công'),
        ('failed', 'Thất bại'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Giao dịch #{self.id} - {self.user.username} - {self.get_status_display()}"
