import os
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
class Achievements(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True, blank=True,null=True)
    image_id = models.IntegerField(null=True, blank=True)
    achievements = models.ManyToManyField(Achievements, blank=True)
    badges = models.ManyToManyField(Badge, blank=True)
    assessment_ids = models.CharField(max_length=10, blank=True)
    assessment_count = models.IntegerField(default=0)
    assessment_streak = models.IntegerField(default=0,null=True,blank=True)
    distance_traveled = models.IntegerField(default=0,null=True,blank=True)
    achievements_completed = models.IntegerField(default=0,null=True,blank=True)
    badges_earned = models.IntegerField(default=0,null=True,blank=True)
    mistery_boxes_earned = models.IntegerField(default=0,null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    token_generated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.username} ({self.email})'

    def get_formatted_phone_number(self):
        # Format the phone number as desired
        return f"{self.phone_number[:3]}-{self.phone_number[3:6]}-{self.phone_number[6:]}"

        
class BikeRackData(models.Model):
    site_ID = models.CharField(max_length=50)
    boroname = models.CharField(max_length=50)
    rackType = models.CharField(max_length=50)
    latitude = models.FloatField()  
    longitude = models.FloatField()  
    newPosition = models.JSONField(max_length=50)
    condition = models.CharField(max_length=50, null=True, blank=True)
    user = models.CharField(max_length=50, null=True, blank=True)  
    assessment = models.CharField(max_length=120, null=True, blank=True)  
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site_ID}"


class NewMarker(models.Model):
    latitude = models.DecimalField(max_digits=30, decimal_places=15)
    longitude = models.DecimalField(max_digits=30, decimal_places=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

class DeleteMarker(models.Model):
    marker_id = models.CharField(max_length=20, unique=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.marker_id})"

# class EditMarkerPosition(models.Model):
#     latitude = models.DecimalField(max_digits=30, decimal_places=15)
#     longitude = models.DecimalField(max_digits=30, decimal_places=15)
#     created_at = models.DateTimeField(auto_now_add=True)