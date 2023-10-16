from django.db import models
from django.contrib.auth.models import User
from blog.models import Post


# Create your models here.
class Subscription(models.Model):
    user = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

    class Meta:
        unique_together = ('user', 'author')


class Notification(models.Model):
    user = models.CharField(max_length=100)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
