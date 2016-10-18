from __future__ import unicode_literals
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
import uuid


class InfoModel(models.Model):
    title = models.CharField(max_length=200)
    blurb = models.TextField()
    rich_text = RichTextField()
    pdf_file = models.FileField(upload_to="pdf_files", blank=True, null=True)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('news-page', kwargs={'pk': str(self.id)})

    def save(self, *args, **kwargs):
        if self.pdf_file:
            self.pdf_file.name = str(uuid.uuid4()) + self.pdf_file.name
            super(InfoModel, self).save(*args, **kwargs)
        else:
            super(InfoModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{}".format(self.title)
