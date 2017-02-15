from __future__ import unicode_literals
import uuid as uuid
from django.db import models
from django.template.defaultfilters import slugify


class Geospace(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'geospaces'

    def __str__(self):
        return str(self.latitude) +','+ str(self.longitude)


class Post(models.Model) :
    name = models.CharField(max_length=250, verbose_name='name of post')
    geospace = models.OneToOneField('Geospace', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    slug = models.SlugField(null=True, editable=False)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.name

    def save(self, *args):
        self.slug = slugify(self.name)
        super(Post, self).save(*args)

class Morcha(models.Model) :
    name = models.CharField(max_length=250, verbose_name='name of morcha')
    geospace = models.OneToOneField('Geospace', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='morchas', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    slug = models.SlugField(null=True, editable=False)

    class Meta:
        db_table = 'morchas'

    def __str__(self):
        return self.name + ":" + str(self.uuid)

    def save(self, *args):
        self.slug = slugify(self.name)
        super(Morcha, self).save(*args)

class Intrusion(models.Model):
    morcha = models.ForeignKey('Morcha', on_delete=models.CASCADE, related_name='morcha')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post')
    detected_datetime = models.DateTimeField()
    verified_datetime = models.DateTimeField(null=True, blank=True)
    neutralized_datetime = models.DateTimeField(null=True, blank=True)
    non_human_intrusion_datetime = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField()

    class Meta:
        db_table = 'intrusions'

    def __str__(self):
        return str(self.detected_datetime) + '-' + self.morcha.name
