from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from metadata.models import Music
from metadata.util import validate_required_fields


class MusicViewSet(viewsets.ViewSet):
    queryset = Music.objects.all()

    @action(detail=False, permission_classes=[permissions.AllowAny])
    def get_music_by_iswc(self, request):
        """
        Intentionally used the 'filter' queryset below instead of 'get', since the iswc field in the database is not
        unique and avoiding a possible MultipleObjectReturned Error that my be thrown with the 'get' queryset.
        """
        try:
            iswc = self.request.query_params.get('iswc')
            if message := validate_required_fields({'iswc': iswc}):
                return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
            music_list = list(Music.objects.filter(iswc=iswc, is_deleted=False).values())
            return JsonResponse(music_list, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
