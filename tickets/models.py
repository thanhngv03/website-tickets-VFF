import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from matches.models import Match


class Seat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.match.title} - Ghế {self.seat.seat_number}"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        first_save = self.pk is None
        super().save(*args, **kwargs)

        # Chỉ tạo QR code nếu là save đầu tiên hoặc chưa có
        if first_save or not self.qr_code:
            data = f"VFF | Vé #{self.id} | {self.user.username} | {self.match.title} | Ghế: {self.seat.seat_number}"
            qr_img = qrcode.make(data)
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            filename = f"ticket-{self.id}.png"
            self.qr_code.save(filename, File(buffer), save=False)

            # Lưu lại lần 2 để ghi qr_code
            super().save(update_fields=["qr_code"])

    def __str__(self):
        return f"Vé #{self.id} - {self.user.username} - {self.match.title}"
