from datetime import datetime, date
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import datetime

# Author: 2327846P - Veronika
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	add_users = models.BooleanField(blank=False, default=False)
	manage_logs = models.BooleanField(blank=False, default=False)
	manage_resources = models.BooleanField(blank=False, default=False)

	def __str__(self):
		return self.user.username


# Author: 2133861W - Andrew
# Editted: 2327846P - Veronika
class Log(models.Model):
	log_id = models.CharField(max_length=32, blank=False, unique=True, null=False)
	guid = models.CharField(max_length=10, default="No GUID", blank=True, null=True)
	topic_discussed = models.CharField(max_length=50, default='student conversation')
	conversation_time = models.DateTimeField('date published', default=datetime.now)
	log = models.CharField(max_length=50000, null=True)
	slug = models.SlugField(unique=True, default='log')

	def save(self, *args, **kwargs):
		self.slug = slugify(self.log_id)
		super(Log, self).save(*args, **kwargs)

	def __str__(self):
		return self.log_id


# Author: 2327846P - Veronika
class Resource(models.Model):
	name = models.CharField(null=False, unique=True, max_length=128)
	file = models.FileField(upload_to='resources', null=False)
	slug = models.SlugField(unique=True, default='resource')

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Resource, self).save(*args, **kwargs)

	def __str__(self):
		return self.name