from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def special(request):
    return HttpResponse("You are loged in.")

@login_required                         # in order to require user to login, then this works
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

     registered = False

     if request.method == "POST":
         user_form = UserForm(data = request.POST)
         profile_form = UserProfileInfoForm(data = request.POST)

         if user_form.is_valid() and profile_form.is_valid():
             user = user_form.save()             # grabbig the user_form and saving it to database
             user.set_password(user.password)    # hashing the password by set_password method
             user.save()                         # saving the hash password to the database

            # FOR THE ATTRIBUTES PORTFOLIO_LINK AND PROFILE_PIC

             profile = profile_form.save(commit = False)
             profile.user = user                   # one to one relationship from User from models.py

            # CHECKING FOR PROFILE PIC
            # if saving any files like PDF,CSV,RESUME, etc, use request.FILES

             if 'profile_pic' in request.FILES:
                 profile.profile_pic = request.FILES['profile_pic']

             profile.save()

             registered = True

         else:
             print(user_form.errors, profile_form.errors)

     else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

     return render(request, 'basic_app/registration.html', {'user_form':user_form,
                                                            'profile_form':profile_form,
                                                            'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')                 # grab username from login.html
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)       # autometically authenticate the user

        if user:                                # if the user is present
            if user.is_active:                  # if the user is active or not
                login(request,user)             # for login user, it will take request and the user object return by authenciate
                return HttpResponseRedirect(reverse('index'))     # once user is login, redirect to some page

            else:
                return HttpResponse("Account not active!")

        else:
            print("someone tried to login and failed!")
            print("Username: {} and password:{}".format(username,password))
            print("Invalid details!")

    else:
        return render(request, 'basic_app/login.html', {})
