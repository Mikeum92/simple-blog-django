from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    #setting publication date method
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    #to redirect author to post_detail view page  after publishing a post
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    #string representation of the model
    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    #to send user back to list of all posts after she/he posts a comment/tell the browser where to go back to
    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
