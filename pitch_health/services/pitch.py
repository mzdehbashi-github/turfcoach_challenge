import datetime
from typing import List, Union

from django.utils import timezone
from django.db.models import Q, Count, QuerySet
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from result import Ok, Err, Result

from pitch_health.models import Pitch, WeatherForecast


def find_next_maintenance_date(pitch_id: int) -> Result[datetime.date, str]:
    """
    Finds the next possible maintenance date for the given pitch_id.

    How it works: Iterates through the related weather forecasts(same location)
    and Checks if the current day doesn't rain and the required number of previous days
    (variable consecutive_dry_days_required) also don't have rain. If conditions are met,
    updates the pitch's next scheduled maintenance date and return it. If no suitable date
    is found, return an error message.
    """
    consecutive_dry_days_required = 2
    today = timezone.now().date()
    queryset = Pitch.objects.select_for_update()
    with (transaction.atomic()):
        pitch = queryset.get(id=pitch_id)
        weather_forecasts: List[WeatherForecast] = list(
            WeatherForecast.objects.filter(
                date__gte=today - datetime.timedelta(consecutive_dry_days_required),
                location=pitch.location
            ).order_by('date')
        )

        for i in range(len(weather_forecasts)):
            # Check if the current day doesn't rain and the required number of previous days also don't have rain
            weather_forecast = weather_forecasts[i]
            if weather_forecast.date >= today and \
                    not weather_forecast.daily_will_it_rain and \
                    i >= consecutive_dry_days_required:

                # Check the previous consecutive_dry_days_required days
                has_consecutive_dry_days = True
                for j in range(1, consecutive_dry_days_required + 1):
                    previous_weather_forecast = weather_forecasts[i - j]
                    if previous_weather_forecast.daily_will_it_rain:
                        has_consecutive_dry_days = False
                        break

                if has_consecutive_dry_days:
                    weather_forecast = weather_forecasts[i]
                    pitch.next_scheduled_maintenance = weather_forecast.date
                    pitch.save(update_fields=('next_scheduled_maintenance',))
                    return Ok(pitch.next_scheduled_maintenance)

        return Err(_('Could not find a date for next scheduled maintenance'))


def update_current_condition(pitch_id: int) -> Result[int, str]:
    """
    Updates current condition of the given pitch according to
    the day of maintenance and weather situation.

    How rating system works: If the maintenance date is today then the
    current_condition is at its best (10) otherwise the value of the current_condition
    is getting calculated according to the amount of days that has been passed since the last maintenance
    and if there was any rainy day in between.
    """
    queryset = Pitch.objects.select_for_update()
    today = timezone.now().date()
    with transaction.atomic():
        pitch = queryset.get(id=pitch_id)
        if last_maintenance_date := pitch.last_maintenance_date:
            current_condition = 10
            if last_maintenance_date < today:
                day_factor: int = (today - last_maintenance_date).days

                # rain has more effect on the current_condition
                rain_factor = WeatherForecast.objects.filter(
                    date__lte=today,
                    daily_will_it_rain=True,
                    date__gte=last_maintenance_date
                ).count() * 1.5

                current_condition -= int(day_factor + rain_factor)

                # just a sanity check
                if current_condition < 0:
                    current_condition = 0

            pitch.current_condition = current_condition
            pitch.save(update_fields=('current_condition',))
            return Ok(current_condition)

    return Err(_('Could not update current condition'))


def find_pitches_in_need_for_maintenance() -> Union[QuerySet, List[WeatherForecast]]:
    """
    Returns pitch records which either have:
        1- low condition (regardless of coming rainy days)
        2- good condition, but will be exposed to rain in the coming days
    """
    today = timezone.now().date()
    locations_with_more_than_three_rainy_days = WeatherForecast.objects.filter(
        date__gte=today,
        daily_will_it_rain=True
    ).values('location').annotate(rainy_days_count=Count('pk')).filter(
        rainy_days_count__gte=3
    ).values_list('location', flat=True)

    return Pitch.objects.filter(
        Q(
            current_condition__lt=5
        ) | Q(
            current_condition__gte=5,
            location__in=locations_with_more_than_three_rainy_days
        ),
    )
