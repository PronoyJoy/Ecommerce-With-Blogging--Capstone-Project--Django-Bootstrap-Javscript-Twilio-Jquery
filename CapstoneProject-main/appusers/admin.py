from django.contrib import admin
from appusers.models import Contact, Follow, Payment,UserProfileInfo


# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Payment)
admin.site.register(Contact)
admin.site.register(Follow)


