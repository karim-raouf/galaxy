from django.shortcuts import render , redirect
from .forms import *
from project.settings import switch_to_user_database
from .models import TestApp
from django.contrib.auth import authenticate , login , logout
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore

# Create your views here.

def apphome(request):
    
    username = request.GET.get('username')
    switch_to_user_database(username)
    
    if request.method == 'POST':
        form = TestForm2(request.POST)
        if form.is_valid():
            form.save()
            form = TestForm2()
            return redirect('App:apphome')
            
    else:
        form = TestForm2()
    
    context = {'form' : form , 'username' : username}
    return render(request , 'App/apphome.html' , context )

def default_db(request):
    default = 'Users'
    switch_to_user_database(default)
    return redirect('galaxy:index')