from django.core.management.base import BaseCommand, CommandError

from pitch_health.services.pitch import find_next_maintenance_date


class Command(BaseCommand):
    help = """
    Finds the next possible maintenance date for the given pitch id
    and updates the related pitch record, accordingly. 
    """

    def add_arguments(self, parser):
        parser.add_argument("pitch_id", type=int)

    def handle(self, *args, **options):
        pitch_id = options["pitch_id"]
        result = find_next_maintenance_date(pitch_id)
        if result.is_err():
            raise CommandError(result.err())
