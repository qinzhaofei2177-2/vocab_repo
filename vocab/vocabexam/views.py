from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .models import Dictionary, UserForm, UserProfileForm, UserProfile

# Create your views here.
def index(request):
    return render(request, "vocabexam/index.html")

def register(request):
    if request.method == 'POST':
        u = UserForm(request.POST, initial=[])
        p = UserProfileForm(request.POST, initial=[])
        if u.is_valid() and p.is_valid():
            # if a user is logged in, log him out!
            if request.user.is_authenticated:
                logout(request)
            # create a new user
            user = u.save(commit=False)
            password = u.cleaned_data['password']
            user.set_password(password)
            user.save()
            # create a new UserProfile by using created user and POST data
            profile = p.save(commit=False)
            profile.user = User.objects.get(username=u.cleaned_data.get("username")) # request.POST["username"]
            profile.save()
            # login with the new created user info
            userlogin = authenticate(request, username=u.cleaned_data.get("username"), password=u.cleaned_data.get("password"))
            if userlogin is not None:
                login(request, userlogin)
            # messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse("exam", args=[]))
        else:
            return render(request,"vocabexam/register.html", {'user_form': u,'profile_form': p})
    else:
        u = UserForm()
        p = UserProfileForm()

    return render(request,"vocabexam/register.html", {'user_form': u,'profile_form': p})

def exam(request):
    if not request.user.is_authenticated:
        return render(request, "vocabexam/login.html", {"message": None})
    context = {
        "user": request.user,
    }
    return render(request, "vocabexam/exam.html", context)

def login_view(request):
    if not request.user.is_authenticated:
        return render(request, "vocabexam/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return HttpResponseRedirect(reverse("exam"))

def login_proc(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "vocabexam/login.html", {"message": "** Invalid user."})

def logout_proc(request):
    logout(request)
    return render(request, "vocabexam/login.html", {"message": "Logged out."})


def search(request, pattern="", limit=20):
    if len(pattern.strip()) == 0 or pattern.isdigit():
        return HttpResponse("Sorry, Search pattern CANNOT be empty.")
    else:
        words = Dictionary.objects.filter(BaseWord__icontains=pattern)[:limit]
        if words.count() == 0:
            return HttpResponse(f"Sorry, no words like \"...{pattern}...\" found.")
        else:
            return HttpResponse(words)