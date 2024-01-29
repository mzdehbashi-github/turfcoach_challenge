from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from pitch_health.models import Pitch
from pitch_health.services.pitch import find_pitches_in_need_for_maintenance
from pitch_health.serializers.v1 import PitchSerializer


class PitchViewSet(ModelViewSet):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer

    @action(methods=['GET'], detail=False, url_path='maintenance-soon')
    def get_pitches_in_need_for_maintenance(self, *args, **kwargs):
        queryset = find_pitches_in_need_for_maintenance()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
