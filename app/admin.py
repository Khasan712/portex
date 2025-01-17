from django.contrib import admin
from .models import CodeBase, FeedBack


@admin.register(CodeBase)
class CodeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'rank', 'created_at', 'updated_at')


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
