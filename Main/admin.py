from django.contrib import admin
from .models import Files, Folder


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'folder', 'date', 'size', 'is_trashed')
    list_filter = ('is_trashed', 'date', 'folder')
    search_fields = ('title', 'description')
    readonly_fields = ('id', 'date', 'size')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created')
    search_fields = ('name',)
    readonly_fields = ('id', 'created')
