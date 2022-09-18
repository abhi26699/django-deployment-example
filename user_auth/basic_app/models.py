from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete = models.CASCADE,)

    # additionnal fields

    portfolio_site = models.URLField(blank = True)

    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)  # In order to upload image we have to install pillow library


    def __str__(self):
        return self.user.username
