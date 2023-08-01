from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.contrib import messages
from .models import Chat, Message
import json
# Create your views here.

def index(request):
    user = request.user
    print(user.id)
    chats = Chat.objects.filter(members=user.id)
    if request.user.is_authenticated:
        return render(request, 'index.html', {'chats':chats})
    else:
        return redirect('login')

def login(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print('user:',user)
        if user is not None:
            do_login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or password is wrong!")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        if User.objects.filter(username=username).count() == 0:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('login')
        else:
            messages.info(request, "Username is taken!")
            return render(request, 'signup.html', {})
    else:
        return render(request, 'signup.html', {})

def logout(request):
    do_logout(request)
    return redirect('/login')