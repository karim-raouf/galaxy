from django.shortcuts import render , redirect
from .models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages



# Create your views here.


def index(request):
    if request.method == 'POST':
        if 'email1' in request.POST:
            email = request.POST.get('email1')
            password = request.POST.get('psw')
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()
            return redirect('index')
        elif 'email2' in request.POST:
            email = request.POST.get('email2')
            password = request.POST.get('psw')
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Email or Password is incorrect')
    
    context = {'page_name' : 'Guest'}
    return render(request , 'galaxy/index.html' , context)



def home(request):
    
    context = {'page_name' : 'Home'}
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


def signout(request):
    
    logout(request)
    return redirect('index')


