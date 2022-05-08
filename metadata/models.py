import uuid

from django.db import models


class TableMetaData(models.Model):
    created_by = models.CharField(max_length=150, blank=True, null=True)  # saves user id here if exists
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=150, blank=True, null=True)  # saves user id here if exists
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)  # saves user id here if exists
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Music(TableMetaData):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    title = models.CharField(max_length=256, blank=True, default='')
    contributors = models.TextField(blank=True, default='')
    iswc = models.CharField(max_length=128, blank=True, default='')

    def __str__(self):
        return f'{self.id} {self.title}'
