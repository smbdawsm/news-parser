from django.db import models
from datetime import datetime
from django import utils


class Article(models.Model):

    title = models.CharField('Title', max_length=255, null=True)
    description = models.CharField('Description', max_length=255, null=True)
    article = models.TextField('Article', default='-')
    image = models.CharField('Image', max_length=1024, null=True)
    url = models.URLField('Original URL')
    date_create = models.DateTimeField('Date created', default=utils.timezone.now)

    class Meta:
        ordering = ['-date_create']
