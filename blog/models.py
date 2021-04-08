from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200, help_text='Enter a tite of blog')
    # Foreign Key used because blog can only have one blogger, but blogger can have multiple blogs
    blog_author = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000, blank=True)
    post_date = models.DateField(null=True, blank=True)
 
    def __str__(self):
        """String for representing the Model object."""
        return self.title

class Blogger(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bio_information = models.TextField(max_length=1000, help_text='Enter a biographical information about the blogger/author')

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

class Comment(models.Model):
    ''' Model representing a comment by a user for a blog'''
    description = models.TextField(max_length=1000, help_text='Enter the comment about the blog')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.blog.title})'