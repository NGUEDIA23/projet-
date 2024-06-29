# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

class Article(models.Model):
   title = models.CharField(max_length=200, verbose_name=_('Title'))
content = models.TextField(verbose_name=_('Content'))
publication_date = models.DateTimeField(verbose_name=_('Publication Date'))

def __str__(self):
        return self.title

