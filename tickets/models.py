import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models

class Ticket(models.Model):
    ...
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Tạo nội dung QR
        data = f"VFF | Vé #{self.id} | {self.user.username} | {self.match.title} | Ghế: {self.seat.seat_number}"
        qr = qrcode.make(data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')

        self.qr_code.save(f"ticket-{self.id}.png", File(buffer), save=False)
        super().save(update_fields=["qr_code"])
