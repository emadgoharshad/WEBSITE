from django.db import models

from users.models import User

class Video(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,)
    desc = models.TextField()
    file = models.FileField(upload_to='videos')
    pub_date = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)

    def __str__(self):
        return self.title

    def count_like(self):
        return self.likes.count()


class Subscriber(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User,related_name='subscribers')
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)



