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

#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u) [0])



# Admin

class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'username', 'anonymous', 'private', 'network' )
    fields = ["username", "anonymous", "private", "body", "network"]

admin.site.register(Post, PostAdmin)

