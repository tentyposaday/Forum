from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posts")
    thread = models.ForeignKey('Thread', on_delete=models.SET_NULL, null=True, related_name="posts")
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.title[:20]
    class Meta:
        ordering = ['-created_at']
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(thread=self.thread, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Comment(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    class Meta:
        ordering = ['created_at']

class Thread(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # Only generate slug if it hasn't been set yet
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Call the original save method
