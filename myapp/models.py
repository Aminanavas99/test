from django.db import models

# Create your models here.

class Role(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user',unique=True)

class User(models.Model):
    name=models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True, null=True, blank=True)

    role=models.ForeignKey(Role, on_delete=models.CASCADE, null=True, default=None)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)



class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)







