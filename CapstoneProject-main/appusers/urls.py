from os import name
from appusers.models import Contact
from django.urls import path
from .import views
from appusers.views import FollowDoneView,UnfollowDoneView
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('follow/done/', login_required(FollowDoneView.as_view()), name='follow_done_view'),
    path('unfollow/done/', login_required(UnfollowDoneView.as_view()), name='unfollow_done_view'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('contact/',views.ContactCreateView.as_view(),name='contact'),
    
 

]