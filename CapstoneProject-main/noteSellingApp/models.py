from django.db import models
from django.template.defaultfilters import slugify, title
from django.urls import reverse
from django.contrib.auth.models import User
import os

# Create your models here.
class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Course(models.Model):
    course_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    institute = models.CharField(max_length=50 ,blank=True)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='course_background_image', blank=True, verbose_name='Course Image')
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_id)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='lessons')
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField(blank=True,null=True)
    code = models.IntegerField(default='2901', editable=False)
   
    slug = models.SlugField(null=True, blank=True)

    image1 = models.ImageField(upload_to='Lesson_carousol_image', blank=True, verbose_name='lesson pdf Image1')
    image2 = models.ImageField(upload_to='Lesson_carousol_image', blank=True, verbose_name='lesson pdf Image2')
    image3 = models.ImageField(upload_to='Lesson_carousol_image', blank=True, verbose_name='lesson pdf Image3')


    lesson_video = models.FileField(upload_to="lesson_video_files",verbose_name="lesson_Video", blank=True, null=True)

    Notes = models.FileField(upload_to='lesson pdf file',verbose_name="Notes", blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('noteSellingApp:lesson_list', kwargs={'slug':self.course.slug, 'standard':self.Standard.slug})


class Review(models.Model):
    lesson_name = models.ForeignKey(Lesson,null=True, on_delete=models.CASCADE,related_name='reviews')

    rev_name = models.CharField(max_length=100, blank=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE)

    body = models.TextField(max_length=500)

    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.rev_name = slugify("Review by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.rev_name

    class Meta:
        ordering = ['-date_added']


class Codetable(models.Model):
    lesson=models.CharField(max_length=100,blank=True)
    code = models.CharField(max_length=100 ,blank=True,null=True)
    
   
