from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add = True)
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return f'Post {self.id} - {self.title}'
    
    class Meta:
        db_table = 'posts'
        db_table_comment = 'Something like blog posts'
        ordering = ['date_posted']

class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateField(auto_now_add = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

    def __str__(self):
        return f'Comment {self.id} from post {self.post.id}'

    class Meta:
        db_table = 'comments'
        db_table_comment = 'Something like comments blog posts'
        ordering = ['date_posted']
