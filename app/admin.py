from django.contrib import admin
from .models import CodeBase, FeedBack, DownloadApp


@admin.register(CodeBase)
class CodeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'rank', 'created_at', 'updated_at')


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')


@admin.register(DownloadApp)
class DownloadAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
