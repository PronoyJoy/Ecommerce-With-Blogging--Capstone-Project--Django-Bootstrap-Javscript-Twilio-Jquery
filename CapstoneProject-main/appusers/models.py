from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.deletion import CASCADE
from django.urls import reverse
from twilio.rest import Client
from phonenumber_field.modelfields import PhoneNumberField
from crum import get_current_user


# Create your models here.

class UserProfileInfo(models.Model):

    #creating a relationship with user class (not inheriting)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #adding additional attributes

    email = models.EmailField(max_length=30,blank=True)
    university = models.CharField(max_length=70, blank=True)
    subject = models.CharField(max_length=70,blank=True)
    expertise = models.CharField(max_length=70,blank=True)
    phone = PhoneNumberField(blank=True,null=True)
    profile_pic = models.ImageField(upload_to= "media/user_profile_pictures", verbose_name="Profile Picture", blank=True ,null = True,)
    facebooklink = models.CharField(max_length=200,blank=True,null=True)
    instalink = models.CharField(max_length=200,blank=True,null=True)
    linkedlink = models.CharField(max_length=200,blank=True,null=True)
    websitelink =models.CharField(max_length=200,blank=True,null=True)
  
    teacher = 'teacher'
    student = 'student'
    
    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
    ]
    user_type = models.CharField(max_length=10, choices=user_types, default=student)

    def __str__(self):
        return self.user.username

    @property
    def follower_count(self):
        count = self.user.follow_followed.count()
        return count

    @property
    def following_count(self):
        count = self.user.follow_follower.count()
        return count
    
   
#follow model

class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow_follower', editable=False)
    followed = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follow_followed')
    is_Follow = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user} --> {self.followed}"


    def save(self,*args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        super(Follow, self).save(*args, **kwargs)


 

    

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    feedback = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')

class Payment(models.Model):
    Payment_id=models.CharField(max_length=100,unique=True)
    buyer_name=models.CharField(max_length=20)
    note_name =models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    mobile_banking_number = models.CharField(max_length=14)

    def __str__(self) -> str:
        return self.Payment_id

    def save (self, *args, **kwargs):


        if self.price > 5 :
            # Find your Account SID and Auth Token at twilio.com/console
            # and set the environment variables. See http://twil.io/secure
            account_sid = 'ACd2b8a7e0e8af66f8f6208a28553abead'
            auth_token = '411a39efe05ef0b1041f6c0fe585e03b'
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                body=" Thanks For Buying The Note \n Your Code is 2901 ",
                                from_='+12017204103',
                                to= '+8801783311800'
                            )

            print(message.sid)


        return super().save(*args, **kwargs)
    
