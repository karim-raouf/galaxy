from django.shortcuts import render , redirect
from .models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from .database_utils import create_user_database
from .database_configuration_utils import update_database_configuration
from .database_connection import get_database_connection
from.make_db_migrations import migrate_to_database
from project.settings import switch_to_user_database
from django.contrib.auth.decorators import login_required
import subprocess
from django.db import connections
# Create your views here.

def index(request):
               
    user = request.user 
    context = {'user' : user}
    return render(request , 'galaxy/index.html' , context)



def home(request):
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
            form = TestForm()
            return redirect('galaxy:index')
            
    context = {'page_name' : 'Home' , 'form' : form}
    return render(request , 'galaxy/home.html' , context)


def about_us(request):
    
    context = {'page_name' : 'About-us'}
    return render(request , 'galaxy/about.html' , context)


def pricing(request):
    
    context = {'page_name' : 'Pricing'}
    return render(request , 'galaxy/pricing.html' , context)


def contact_us(request):
    
    context = {'page_name' : 'Contact-us'}
    return render(request , 'galaxy/contact.html' , context)

#--------------------------------------------------------------------------------

# @login_required
# def make_migrations():
#     # Run migrations for the current database
#     call_command('makemigrations')
#     call_command('migrate')

def login_page(request):
    errors = []
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('psw')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('galaxy:index')
            else:
                errors.append("Incorrect Password!")
        except :
            errors.append("Incorrect Email address!")
    
    context = {'errors': errors}
    return render(request, 'galaxy/login.html', context)

def signup_page(request):
    errors = []
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('psw')
        username = request.POST.get('user_n')
        try:
            user = User.objects.get(email=email)
            errors.append('Email already associated with another account!')
        except:
            user = User.objects.create(email=email, username=username)
            user.set_password(password)
            user.save()
            create_user_database(user.username)

            #---- Switch to the user's database
            # connections['default'].close()
            # connections['default'].settings_dict['NAME'] = user.username
            # connections['default'].cursor()
            #switch_to_user_database(user.username)

            # -----Run the migration command
            #subprocess.run(['python', 'manage.py', 'migrate', '--database=' + 'default'])

            #----- Switch back to the default database
            # connections['default'].close()
            # connections['default'].settings_dict['NAME'] = 'Users'
            # connections['default'].cursor()
            #switch_to_user_database('Users')
            return redirect('galaxy:login')
    else:
        errors = []

    context = {'errors': errors}
    return render(request, 'galaxy/register.html', context)




def signout(request):
    
    logout(request)
    return redirect('galaxy:index')


