from django.db import models

class Match(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='matches/')
    ticket_price = models.PositiveIntegerField()

    def __str__(self):
        return self.title
