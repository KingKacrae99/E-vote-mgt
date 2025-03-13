from django.db import models
from django.contrib.auth.models import AbstractUser
from .manages import MemberManager
from django.utils.text import slugify
from django.shortcuts import HttpResponse
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import os

# Create your models here.
class Member(AbstractUser):
    username = None
    password = models.CharField(max_length=128, default="default_password")
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField('is_admin', default=False, blank=True)
    phone = models.CharField(max_length=15, blank=False, null=True, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = MemberManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Position(models.Model):
    title = models.CharField(max_length=200,unique=True)
    descript= models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(unique=True,blank=True)

    def __str__(self):
        return self.title

    def save (self, *args, **kwargs):
        if not self.slug:
           self.slug = slugify(self.title)
        super().save(*args,**kwargs)


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="candidates")
    profile_pic = models.ImageField(default="images/default_user_icon.jpg", upload_to="images/%Y/", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnail/%Y/", null=True, blank=True ,editable=False)
    profile = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save first to get an ID
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.id}")
            super().save(*args, **kwargs)  # Save again to update the slug



class Vote(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="members")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes")
    timestamp = models.DateTimeField(auto_now_add=True)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} voted for {self.candidate.name}"