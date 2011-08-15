from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Post(models.Model):
    username = models.CharField(max_length=20)
    network = models.CharField(max_length=20)
    anonymous = models.BooleanField()
    private = models.BooleanField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=20)
    website_url = models.CharField(max_length=40)
    facebook_url = models.CharField(max_length=40)
    twitter_url = models.CharField(max_length=40)

class ProfileImage(models.Model):
	user = models.ForeignKey(User)
	image = models.ImageField(upload_to='images/avatars/')

class Comment(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	author = models.CharField(max_length=60)
	anonymous = models.BooleanField()
	body = models.TextField()
	post = models.ForeignKey(Post)
	
class PostImage(models.Model):
	post = models.ForeignKey(Post)
	image = models.ImageField(upload_to='images/posts/')
	

# Admin

class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'username', 'anonymous', 'private', 'network' )
    fields = ["username", "anonymous", "private", "body", "network"]

class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'post', 'created')
	fields = ["author", "post", "body"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

