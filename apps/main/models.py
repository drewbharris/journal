from django.db import models
from django.contrib import admin

class Post(models.Model):
	username = models.CharField(max_length=20)
	anonymous = models.BooleanField()
	private = models.BooleanField()
	image = models.BooleanField()
	body = models.TextField()
	created = models.DateTimeField()

	def __unicode__(self):
		return self.username

class Test(models.Model):
	test = 'test message'
	def __unicode__(self):
		return self.test

# Admin

class PostAdmin(admin.ModelAdmin):
	list_display = ('anonymous', 'private', 'image', 'username', 'created')
	fields = ["username", "anonymous", "private", "image", "created", "body"]

admin.site.register(Post, PostAdmin)
