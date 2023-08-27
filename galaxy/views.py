from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .database_utils import create_user_database
from .database_configuration_utils import update_database_configuration
from .database_connection import get_database_connection
from.make_db_migrations import migrate_to_database
from project.settings import switch_to_user_database
from django.contrib.auth.decorators import login_required
import subprocess
from django.db import connections
from datetime import datetime, timedelta
# for email sending----------------------------------------
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_str
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
# Create your views here.

def index(request):
    switch_to_user_database('Users')
    org_num = 0
    try:
        all_orgs = request.user.organization_set.all()
        for org in all_orgs:
            org_num += 1
    except:
        all_orgs = None
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
    context = {'user' : user , 'subed' : subed , 'org' : org , 'org_num' : org_num }
    return render(request , 'galaxy/index.html' , context)



def about_us(request):
    switch_to_user_database('Users')
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
    context = {'page_name' : 'About-us' , 'subed' : subed , 'org' : org}
    return render(request , 'galaxy/about.html' , context)

def get_user_organizations(user_id):
    user = User.objects.get(id=user_id)
    organizations = Organization.objects.filter(UserID=user)
    return organizations

def choose_org(request):
    user = request.user
    organizations = get_user_organizations(user.id)
    
    if request.method == 'POST':
        organization_id = request.POST.get('organization')
        organization = Organization.objects.get(id = organization_id)
        user.OrganizationID = organization
        user.save()
        return redirect('galaxy:index')
    else:
        organizations = get_user_organizations(user.id)
        
    
    context = {'organizations' : organizations}
    return render(request , 'galaxy/org_choose.html' , context)


def pricing(request):    
    switch_to_user_database('Users')
    plan_1 = None
    plan_2 = None
    plan_3 = None
    user = request.user
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(Status = True , OrganizationID = org)
        plan_1 = Subscription.objects.filter(PlanID = 1 , OrganizationID = org , UserID = user)
        plan_2 = Subscription.objects.filter(PlanID = 2 , OrganizationID = org , UserID = user)
        plan_3 = Subscription.objects.filter(PlanID = 3 , OrganizationID = org , UserID = user)
    except:
        subed = False
    
    
    context = {'page_name' : 'Pricing' , 'subed' : subed , 'plan_1' : plan_1 , 'plan_2' : plan_2 , 'plan_3' : plan_3 , 'org' : org}
    return render(request , 'galaxy/pricing.html' , context)

@login_required
def payment(request , id):
    user = request.user
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=30)
    org_id = user.OrganizationID
    if request.method == 'POST':
        if 'payment_btn' in request.POST: 
            try:
                usersub = Subscription.objects.get(UserID = user.id , Status = True , OrganizationID = org_id) # if subscription is active update it
                usersub.PlanID = id
                usersub.StartDate = current_date
                usersub.EndDate = end_date
                usersub.save()
                return redirect('galaxy:u_success_m')
            except:                                                             # if not create one
                Subscription.objects.create( UserID = user, Status = True , PlanID = id , AutoRenew = False , StartDate = current_date, EndDate = end_date , OrganizationID = org_id )
                create_user_database(str(org_id)+'_'+str(user.id))
                return redirect('galaxy:success_m')
    context = {}
    return render(request , 'galaxy/payment.html' , context)

def success(request):
    template = render_to_string('galaxy/email_message.html' ,{'name' : request.user.username})
    
    email = EmailMessage(
        'Thanks for subscribing',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = False
    email.send()
    context = {}
    return render(request , 'galaxy/subscribe_success.html' , context)

def update_success(request):
    template = render_to_string('galaxy/update_message.html' ,{'name' : request.user.username})
    
    email = EmailMessage(
        'Thanks for upgrading bundle',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    email.fail_silently = False
    email.send()
    context = {}
    return render(request , 'galaxy/update_success.html' , context)


def contact_us(request):
    switch_to_user_database('Users')
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
    context = {'page_name' : 'Contact-us' , 'subed' : subed , 'org' : org}
    return render(request , 'galaxy/contact.html' , context)


def profile(request):
    user = User.objects.get(id = request.user.id)
    if request.method == 'POST':
        return redirect('galaxy:profile_edit')
    
    context = {'user' : user}
    return render(request , 'galaxy/profile.html' , context)


def profile_edit(request):
    user = request.user
    form = ProfileForm(instance=user)
    if request.method =='POST':
        form = ProfileForm(request.POST , request.FILES , instance=user)
        if request.POST.get('first_name').isnumeric() or request.POST.get('last_name').isnumeric():
            messages.error(request, 'First/Last Name Can’t Be Entirely Numeric')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if not request.POST.get('first_name') or not request.POST.get('last_name'):
            messages.error(request, 'Do Not Leave First/Last Name Blank')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            if form.is_valid():
                form.save()
                return redirect('galaxy:profile')
    context = {'form' : form}
    return render(request , 'galaxy/profile_edit.html' , context)

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
        user = User.objects.get(email=email)
        print(user.is_active)
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('galaxy:org_choose')
            else:
                errors.append("Incorrect Password!")
        except :
            errors.append("Incorrect Email address!")
    
    context = {'errors': errors}
    return render(request, 'galaxy/login.html', context)

def activate(request , uidb64 , token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user , token):
        user.is_active = True
        user.save()
        
        messages.success(request , 'your email is successfully activated, now youc an login.')
        return redirect('galaxy:activate_done') 
    else:
        messages.error(request , 'Activation link is invalid!')
    return redirect('galaxy:index')   
    
    
    
def active_email(request , user , to_email):
    mail_subject = 'Activate your account.'
    message = render_to_string('galaxy/activation_email.html' , {
        'user': user.username , 
        'domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user),
        'protocol' : 'https' if request.is_secure() else 'http'
        })
    email = EmailMessage(mail_subject , message , to=[to_email])
    email.send()
    # if email.send():
    #     messages.success(request , f'Dear , <b>{user}</b> , please go to your email <b>{to_email}</b> inbox\
    #     and click on received activation link to confirm and complete the registration<b>Note:</b>\
    #     check the spam folder.')
    # else:
    #     message.error(request , f'problem sending email to {to_email}, check if you typed it correctly.')

def signup_page(request):
    errors = []
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('psw')
        username = request.POST.get('user_n')
        organization = request.POST.get('org_n')
        current_date = datetime.now().date()
        try:
            user = User.objects.get(email=email)
            errors.append('Email already associated with another account!')
        except:
            
            user = User.objects.create(email=email, username=username)
            user.set_password(password)
            user.save()
            user.is_active = False
            user.save()
            active_email(request , user , email)
            
            org = Organization.objects.create(UserID=user , OrganizationName=organization , CreatedDate=current_date)
            userr = User.objects.get(email = email)
            userr.OrganizationID = org
            userr.save()
            
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
            return redirect('galaxy:activate_msg')
    else:
        errors = []

    context = {'errors': errors}
    return render(request, 'galaxy/register.html', context)




def signout(request):
    
    logout(request)
    return redirect('galaxy:index')

def activation_msg(request):
    context = {}
    return render(request , 'galaxy/activation_msg.html' , context)

def activation_done(request):
    if request.method == 'POST':
        return redirect('galaxy:login')
    context = {}
    return render(request , 'galaxy/activation_done.html' , context)


