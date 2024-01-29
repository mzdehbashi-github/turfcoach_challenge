from rest_framework import serializers

from pitch_health.models import Pitch


class PitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = (
            'id',
            'pitch_name',
            'location',
            'turf_type',
            'last_maintenance_date',
            'next_scheduled_maintenance',
            'current_condition',
        )
