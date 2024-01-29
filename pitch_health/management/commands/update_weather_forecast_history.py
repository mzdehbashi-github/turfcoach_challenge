import datetime

from django.core.management.base import BaseCommand, CommandError

from pitch_health.services.weather_forecast import update_weather_forecast_history


class Command(BaseCommand):
    help = """
        Fetches the history data from Weather API for the given city
        and stores them in database.
        You need to also provide start and end date
        """

    def add_arguments(self, parser):
        parser.add_argument("city", type=str)
        parser.add_argument(
            "start_date",
            type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        )
        parser.add_argument(
            "end_date",
            type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
        )

    def handle(self, *args, **options):
        city = options["city"]
        start_date = options["start_date"]
        end_date = options["end_date"]
        result = update_weather_forecast_history(city, start_date, end_date)
        if result.is_err():
            raise CommandError(result.err())
