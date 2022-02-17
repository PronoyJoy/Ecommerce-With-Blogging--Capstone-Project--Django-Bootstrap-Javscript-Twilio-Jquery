from django.contrib import admin
from blogApp.models import Blog,Topic,Post,Comment,Reply

# Register your models here.
admin.site.register(Blog)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)