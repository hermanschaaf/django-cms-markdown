# coding=utf-8

import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField


class Markdown(CMSPlugin):
    content = models.TextField(_('Content'), blank=True)
    css = models.TextField(_('CSS'), blank=True)

@receiver(post_save, sender=Markdown)
def post_save_Markdown(sender, instance, **kwargs):
    if instance.id is not None:
        history_item = MarkdownHistory()
        history_item.markdown = instance
        history_item.content = instance.content
        history_item.css = instance.css
        history_item.save(force_insert=True)

class MarkdownHistory(models.Model):
    markdown = models.ForeignKey(Markdown)
    content = models.TextField(blank=False)
    css = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

class MarkdownImage(models.Model):
    markdown = models.ForeignKey(Markdown)
    alias = models.SlugField(max_length=50)
    image = FilerImageField()

class MarkdownFile(models.Model):
    markdown = models.ForeignKey(Markdown)
    alias = models.SlugField(max_length=50)
    file = FilerFileField()

