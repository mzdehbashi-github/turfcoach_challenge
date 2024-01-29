from django.db import models


class WeatherForecast(models.Model):
    """
    Simplified version of forecast data.

    This model also helps to store data that is coming from an external API
    which can be useful in order to reduce being dependant to an external API
    and also reduce costs of sending HTTP requrests.
    """
    date = models.DateField()
    daily_will_it_rain = models.BooleanField()
    location = models.CharField(max_length=100, help_text="in format of city/country")

    class Meta:
        unique_together = [
            ['date', 'location']
        ]
