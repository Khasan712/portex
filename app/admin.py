import ast
import json
from django.contrib import admin
from .models import CodeBase, FeedBack, DownloadApp


@admin.register(CodeBase)
class CodeBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'rank', 'created_at', 'updated_at')


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'text')


@admin.register(DownloadApp)
class DownloadAppAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'country', 'info')

    def country(self, obj):
        try:
            fixed_info = json.dumps(ast.literal_eval(obj.info))
            info = json.loads(fixed_info)
            return info.get('country')
        except Exception as e:
            print(str(e))
            return '-'
    country.short_description = 'Country'
