from django.shortcuts import render , redirect
from .forms import *
from project.settings import switch_to_user_database
from .models import TestApp
from django.contrib.auth import authenticate , login , logout
from django.core.cache import cache
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse
# Create your views here.

def apphome(request):
    
    orgname = request.GET.get('orgname')
    switch_to_user_database(orgname)
    
    if request.method == 'POST':
        form = TestForm2(request.POST)
        if form.is_valid():
            form.save()
            return redirect('App:apphome')
            
    else:
        form = TestForm2()
    
    context = {'form' : form , 'orgname' : orgname}
    return render(request , 'App/apphome.html' , context )

def default_db(request):
    default = 'Users'
    switch_to_user_database(default) 
    return redirect('galaxy:index')

    
    