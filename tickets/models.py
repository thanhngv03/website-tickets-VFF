import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from matches.models import Match
from django.utils import timezone

class Seat(models.Model):
    SEAT_CHOICES = [
        ('A2', 'Khán đài A2'),
        ('A3', 'Khán đài A3'),
        ('A4', 'Khán đài A4'),
        ('A5', 'Khán đài A5'),
        ('B', 'Khán đài B'),
        ('C', 'Khán đài C'),
        ('D', 'Khán đài D'),
    ]

    PRICES = {
        'A2': 350000,
        'A3': 350000,
        'A4': 300000,
        'A5': 300000,
        'B': 200000,
        'C': 150000,
        'D': 150000,
    }
    code = models.CharField(max_length=20, unique=False, blank=True, null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=2, choices=SEAT_CHOICES)
    is_booked = models.BooleanField(default=False)

    def price(self):
        return self.PRICES.get(self.seat_number, 0)

    def __str__(self):
        return f"{self.match.title} - {self.get_seat_number_display()}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='tickets')
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    date = date = models.DateTimeField(default=timezone.now)

    booked_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"Vé của {self.user.username} - {self.match.title} - Ghế {self.seat.get_seat_number_display()}"

    def price(self):
        return self.seat.price()

    def save(self, *args, **kwargs):
        first_save = self.pk is None

        # Đồng bộ ngày trận từ Match nếu chưa có
        if not self.date:
            self.date = self.match.date  # Lấy ngày từ match

        super().save(*args, **kwargs)

        # Tạo mã QR nếu mới hoặc chưa có
        if first_save or not self.qr_code:
            data = (
                f"Vé #{self.id}\n"
                f"Người dùng: {self.user.username}\n"
                f"Trận đấu: {self.match.title}\n"
                f"Ngày: {self.date.strftime('%d/%m/%Y %H:%M')}\n"
                f"Địa điểm: {self.match.location}\n"
                f"Chỗ ngồi: {self.seat.get_seat_number_display()}\n"
                f"Giá: {self.price():,} VNĐ"
            )
            qr_img = qrcode.make(data)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            self.qr_code.save(f'ticket-{self.id}.png', File(buffer), save=False)
            super().save(update_fields=['qr_code'])