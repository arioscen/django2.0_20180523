from django.db import models


class Bar(models.Model):
    title = models.CharField(max_length=16)
    content = models.CharField(max_length=512)
