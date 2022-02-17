from django.contrib import admin
from django.contrib.admin.helpers import AdminErrorList
from .models import Codetable, Standard,Course,Lesson,Review
# Register your models here.
admin.site.register(Standard)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Review)
admin.site.register(Codetable)