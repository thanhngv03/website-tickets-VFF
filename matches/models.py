from django.db import models
from datetime import time
from django.utils import timezone

class Match(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    start_time = models.TimeField(default=time(19, 15)) 
    end_time = models.TimeField(default=time(21, 15))    
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='matches/')
    ticket_price = models.PositiveIntegerField()

    def is_open_for_sale(self):
        return timezone.now() < self.date

    def __str__(self):
        return self.title