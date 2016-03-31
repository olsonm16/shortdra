from django.db import models
from django.db.models import permalink

class ShortLink(models.Model):
	string = models.CharField(max_length=128, unique=True)
	url = models.URLField()

	def __unicode__(self):
		return self.string

	def get_url(self):
		return self.url

class Author(models.Model):
	username = models.CharField(max_length=128, unique=True)
	first_name = models.CharField(max_length=128, unique=False)
	last_name = models.CharField(max_length=128, unique=False)

class Post(models.Model):
	title = models.CharField(max_length=128, unique=False)
	brief = models.CharField(max_length=128, unique=False)
	author = models.CharField(max_length=128, unique=False)
	body = models.TextField()
	date = models.DateField(auto_now=True)


