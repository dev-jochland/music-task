from django.contrib import admin

from metadata.models import Music


class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'iswc', 'contributors')


admin.site.register(Music, MusicAdmin)
