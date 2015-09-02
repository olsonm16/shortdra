from django import django.db.models.Model

class ShortLink(models.Model):
	string = models.CharField(max_length=128, unique=True)
	url = models.URLField()

	def __unicode__(self):
		return self.string
