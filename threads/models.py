from django.db import models


class Thread(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    opening_post = models.TextField()
    author = models.ForeignKey('auth.User', related_name='threads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
