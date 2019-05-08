from django.db import models
from authors.apps.profiles.models import Profile
from authors.apps.articles.models import Article


class Comment(models.Model):
    """Comment Model"""
    body = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    highlighted_text = models.TextField(null=True)
    start_index = models.PositiveIntegerField(null=True, blank=True)
    end_index = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.body

class CommentLikeDislike(models.Model):
    """Model for like and dislike comment"""

    like = models.BooleanField(default=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.like
