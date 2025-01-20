from django.db import models


class CodeBase(models.Model):
    header = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=300, blank=True, null=True)
    extra_info = models.CharField(max_length=300, blank=True, null=True)
    rank = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.header}'


class FeedBack(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class DownloadApp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'
