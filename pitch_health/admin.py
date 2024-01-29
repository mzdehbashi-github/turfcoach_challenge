from django.contrib import admin

from pitch_health.models import WeatherForecast, Pitch


@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = [
        'location', 'date', 'daily_will_it_rain'
    ]


@admin.register(Pitch)
class PitchAdmin(admin.ModelAdmin):
    list_display = [
        'pitch_name',
        'location',
        'last_maintenance_date',
        'next_scheduled_maintenance',
        'current_condition',
    ]
