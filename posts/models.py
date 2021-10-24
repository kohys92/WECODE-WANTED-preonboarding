from django.db import models


class Posts(models.Model):
    title      = models.CharField(max_length=200)
    author     = models.CharField(max_length=100)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user       = models.ForeignKey('users.User', on_delete = models.CASCADE)

    class Meta:
        db_table = 'posts'