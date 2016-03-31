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

class GermanyStory(models.Model):
	title = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    posted = models.DateField(db_index=True, auto_now_add=True)
	
	@permalink
	def get_absolute_url(self):
		return ('view_story', None, { 'slug': self.slug })
