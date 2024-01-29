from django.core.management.base import BaseCommand, CommandError

from pitch_health.services.pitch import update_current_condition


class Command(BaseCommand):
    help = """
    Updates the current condition (field current_condition) for the given pitch id. 
    """

    def add_arguments(self, parser):
        parser.add_argument("pitch_id", type=int)

    def handle(self, *args, **options):
        pitch_id = options["pitch_id"]
        result = update_current_condition(pitch_id)
        if result.is_err():
            raise CommandError(result.err())
