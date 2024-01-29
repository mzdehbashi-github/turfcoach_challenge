from django.core.management.base import BaseCommand, CommandError

from pitch_health.services.weather_forecast import update_weather_forecast


class Command(BaseCommand):
    help = """
    Fetches the future data from Weather API for the given city
    and stores them in database.
    """

    def add_arguments(self, parser):
        parser.add_argument("city", type=str)
        parser.add_argument("days", type=int)

    def handle(self, *args, **options):
        city = options["city"]
        days = options["days"]
        result = update_weather_forecast(city, days)
        if result.is_err():
            raise CommandError(result.err())
