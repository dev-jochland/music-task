from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from metadata.models import Music


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
            music_list = list(Music.objects.filter(iswc=iswc, is_deleted=False).values())
            return JsonResponse(music_list, safe=False)
        except Exception as e:
            return JsonResponse({'detail': str(e)})
