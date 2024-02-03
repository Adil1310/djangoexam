from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.timezone import now

# Create your models here.

class Post(models.Model):

    class Meta:
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'
        ordering = ['-created_at']
    
    title = models.CharField(max_length=200)
    author= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to="images")
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'
        ordering = ["-dateTime"]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
