import os
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

#blogtype table

class Blog(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


#blog topics table

class Topic(models.Model):
    topic_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='topics')
    image = models.ImageField(upload_to='topic_background_image', blank=True, verbose_name='Topic Image')
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic_id)
        super().save(*args, **kwargs)

#table for posts

class Post(models.Model):
    post_id = models.CharField(max_length=100, unique=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=250)
    article = models.TextField(max_length=10000,blank=True)
    post_image=models.ImageField(upload_to="post_images",verbose_name="Picture", blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to="video_files",verbose_name="Video", blank=True, null=True)
    ppt = models.FileField(upload_to="powerpoint_files",verbose_name="Presentations", blank=True)
    Notes = models.FileField(upload_to="pdf_files",verbose_name="Notes", blank=True)
    link = models.CharField(max_length=500,blank=True)
    youtube_link = models.CharField(max_length=500,blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blogApp:post_list', kwargs={'slug':self.topic.slug, 'blog':self.blog.slug})

   


class Comment(models.Model):
    post_name = models.ForeignKey(Post,null=True, on_delete=models.CASCADE,related_name='comments')

    comm_name = models.CharField(max_length=100, blank=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE)

    body = models.TextField(max_length=500)

    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)