from os import name
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import fields
from appusers.models import Contact, UserProfileInfo
from phonenumber_field.modelfields import PhoneNumberField

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')


        labels = {
        'password1':'Password',
        'password2':'Confirm Password'
        }

class UserProfileInfoForm(forms.ModelForm):
    
    university = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    expertise = forms.CharField(required=False)
    profile_pic =forms.ImageField(required=True)

    teacher = 'teacher'
    student = 'student'

    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
        
    ]
    user_type = forms.ChoiceField(required=True, choices=user_types)

    class Meta():
        model = UserProfileInfo
        fields = ('university','subject','expertise','profile_pic','phone', 'facebooklink','instalink','linkedlink','websitelink', 'user_type',)

class ContactForm(forms.ModelForm):
    class Meta():
        model = Contact
        fields = '__all__'