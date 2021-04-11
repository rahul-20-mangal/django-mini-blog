from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200)
    # Foreign Key used because blog can only have one blogger, but blogger can have multiple blogs
    blog_author = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000, blank=True)
    post_date = models.DateField(null=True, blank=True)
 
    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this blog."""
        return reverse('blog-detail', args=[str(self.id)])

class Blogger(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio_information = models.TextField(max_length=1000, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('blogger-detail', args=[str(self.id)])

class Comment(models.Model):
    ''' Model representing a comment by a user for a blog'''
    description = models.TextField(max_length=1000)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user} ({self.blog})'