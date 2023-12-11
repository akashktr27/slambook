from django.db import models
from account.models import *
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)

    def __str__(self):
        return f'{self.user.email} - {self.created_at}'

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.created_at}'
