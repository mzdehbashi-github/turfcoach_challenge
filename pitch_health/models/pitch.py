from django.db import models
from django.utils.translation import gettext_lazy as _


class Pitch(models.Model):

    class TurfTypeChoice(models.TextChoices):
        NATURAL = "natural", _("natural")
        ARTIFICIAL = "artificial", _("Artificial")
        HYBRID = "hybrid", _("hybrid")

    pitch_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, help_text="in format of 'city/country'")
    turf_type = models.CharField(max_length=12, choices=TurfTypeChoice.choices)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_scheduled_maintenance = models.DateField(null=True, blank=True)
    current_condition = models.PositiveSmallIntegerField(null=True, blank=True)
