from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="title")
    text = models.CharField(max_length=100, verbose_name="text")
    created_date = models.DateField(verbose_name="date", auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    text = models.TextField(verbose_name='comment')

    def __str__(self):
        return self.text


class Login(models.Model):
    text = models.CharField(max_length=100, verbose_name='password')

    def __str__(self):
        return self.text


class PostLike(models.Model):
    post = models.ForeignKey(Post, null=True,
                             on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True,
                             on_delete=models.SET_NULL)
