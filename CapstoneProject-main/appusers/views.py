
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from appusers.forms import ContactForm, UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from appusers.models import Contact, Follow,UserProfileInfo,User
from django.contrib.auth import get_user_model
from django.views.generic import (
     CreateView,View
)


def index(request):
    return render(request,'home.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password )

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")

    else:
        return render(request,'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST ,  request.FILES)
        profile_form = UserProfileInfoForm(request.POST , request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
          
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'profile_form':profile_form})


@login_required
def profile(request,username):
    user = User.objects.get(username=username)
    
    if user:
        profile=UserProfileInfo.objects.get(user=user)
        email = profile.email
        expertise = profile.expertise
        university = profile.university
        user_type =profile.user_type
        user_img = profile.profile_pic
        phone = profile.phone

        data = {
            'profile':profile,
            'user_obj':user,
            'email':email,
            'expertise':expertise,
            'university':university,
            'phone':phone,
            'user_type':user_type,
            'user_img':user_img,
         
        }
        if user == request.user:
            return render(request,'profile.html',data)

    
        elif user != request.user:
            try:
                Follow.objects.get(user=request.user, followed=user)
                is_follows_this_user = True
            except Exception as e:
                is_follows_this_user = False
            data = {
            'profile':profile,
            'user_obj':user,
            'email':email,
            'expertise':expertise,
            'university':university,
            'phone':phone,
            'user_type':user_type,
            'user_img':user_img,
            'is_follows_this_user': is_follows_this_user
         
            }
                    
            return render(request,'profile.html',data)
    


#FOLLOW UNFOLLOW
class FollowDoneView(View):
    def post(self, request, *args, **kwargs):
        followed_user_id = request.POST.get('followed_user_id')
        followed_user_obj = User.objects.get(pk=followed_user_id)

        try:
            Follow.objects.get(user=request.user, followed=followed_user_obj)
        except Exception as e:
            follow_obj = Follow.objects.create(followed=followed_user_obj)

        return redirect(request.META.get('HTTP_REFERER'))


class UnfollowDoneView(View):
    def post(self, request, *args, **kwargs):
        unfollowed_user_id = request.POST.get('unfollowed_user_id')
        unfollowed_user_obj = User.objects.get(pk=unfollowed_user_id)

        try:
            follow_obj = Follow.objects.get(user=request.user, followed=unfollowed_user_obj)
            follow_obj.delete()
        except Exception as e:
            pass

        return redirect(request.META.get('HTTP_REFERER'))



#####################################################################


class ContactCreateView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'contact.html'


