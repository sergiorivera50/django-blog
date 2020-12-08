from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # pass the function timezone.now so that it's not called now but when required
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # if a User is deleted, delete all of their posts
    announcement = models.BooleanField(default=False)  # checkbox

    def __str__(self):
        return self.title + " ann=" + str(self.announcement)

    def get_absolute_url(self):  # tells django how to find the url to any instance of a Post
        return reverse('post-detail', kwargs={'pk': self.pk})  # returns full path as a String


class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.author) + " " + str(self.date_posted)
