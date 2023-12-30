from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=32)
    temperature = models.CharField(max_length=24)
    description = models.TextField()
    icon = models.CharField(max_length=55)
    updated_date = models.DateTimeField()
    api_response = models.TextField()

    def __str__(self):
        return self.city
