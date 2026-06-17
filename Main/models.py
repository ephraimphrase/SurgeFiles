from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    """A single-level folder for organizing files."""
    id = models.CharField(max_length=8, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Files(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    date = models.DateField(auto_now_add=True)
    id = models.CharField(max_length=8, primary_key=True, unique=True)

    # Folder organization
    folder = models.ForeignKey(
        Folder, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='files'
    )

    # Public sharing
    share_id = models.CharField(max_length=16, null=True, blank=True, unique=True)

    # File metadata
    size = models.BigIntegerField(default=0)

    # Soft delete / trash
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Files'

    def __str__(self):
        return self.title or '(untitled)'


import os
from django.dispatch import receiver

@receiver(models.signals.post_delete, sender=Files)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Files` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)