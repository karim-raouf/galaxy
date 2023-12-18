from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .forms import *
from django.http import HttpResponseRedirect ,HttpResponse
from .database_utils import create_user_database , delete_user_database
from .database_configuration_utils import update_database_configuration
from .database_connection import get_database_connection
from.make_db_migrations import migrate_to_database
from project.settings import switch_to_user_database
from django.contrib.auth.decorators import login_required
import subprocess
from django.db import connections
from datetime import datetime, timedelta , time
# for email sending----------------------------------------
from django.core.mail import EmailMessage
from django.conf import settings
import os
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes , force_str
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import secrets
from urllib.parse import urlencode
from django.core.files import File 
import urllib
import re
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import json
from dateutil import parser
from django.contrib.sessions.models import Session
from django.utils import timezone , dateformat
from django.contrib.sessions.backends.db import SessionStore
from django.http import Http404
import phonenumbers
import requests
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
import logging
import uuid  # For generating a unique identifier

# Create your views here.

def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer


def index(request):
    switch_to_user_database('Users')
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # ------------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None

    if request.user.is_authenticated:
        if request.user.user_Type == s_u:
            admin_user = request.user.SubscriptionID.UserID
            su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
            su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
            su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
            su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
        
    # ------------------------------------------------------------------------------
    try:
        user = request.user
        current_date = datetime.now().date()
        update_subscription_status(user, current_date)
    except:
        pass
    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    # -------------------------------------------------------------------
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

    cart_basic = Cart.objects.filter(Bundle_T='Basic')
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
        
    pass_error = []
    
    if request.method == 'POST':
        if 'save-profile' in request.POST:
            userform = ProfileForm(request.POST , request.FILES , instance=request.user)
            if userform.is_valid():
                userform.save()
                messages.success(request, "Profile saved successfully!")
            else:
                
                print(userform.errors)
                
    context = {'user' : user , 'subed' : subed , 'org' : org , 'org_num' : org_num , 'cart' : cart , 'in_cart' : in_cart , 'total' : total , 'cart_basic' : cart_basic , 'userform' : userform , 's_a' : s_a , 's_u' : s_u , 'w_u' : w_u , 'pass_error' : pass_error , 'su_basic_sub' : su_basic_sub , 'su_user_sub' : su_user_sub , 'su_org_sub' : su_org_sub , 'su_store_sub' : su_store_sub}
    return render(request , 'galaxy/index.html' , context)
#update user--------------------------------------------------------------------------------------------------------------------------------------
def update_subscription_status(user, current_date):
    Subscription.objects.filter(UserID=user, EndDate=current_date).update(Status=False)
#--------------------------------------------------------------------------------------------------------------------------------------------------

def about_us(request):
    switch_to_user_database('Users')
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # --------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None
    
    try:
        admin_user = request.user.SubscriptionID.UserID
        su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
        su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
        su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
        su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
    except:
        pass

    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    #--------------------------------------------------------
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
    #------------- for buttton disable if no cart basic in cart or subscription----------------------------   
    cart_basic = Cart.objects.filter(Bundle_T='Basic')    
    #------- for user profile form-------------------
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
    
    pass_error = []
    
    if request.method == 'POST':
        if 'save-profile' in request.POST:
            userform = ProfileForm(request.POST , request.FILES , instance=request.user)
            if userform.is_valid():
                userform.save()
                messages.success(request, "Profile saved successfully!")
    #-----------------------------------------------------------
    context = {'page_name' : 'About-us' , 'subed' : subed , 'org' : org , 'in_cart' : in_cart , 'cart' : cart , 'total' : total , 'cart_basic' : cart_basic , 'userform' : userform , 's_a' : s_a , 's_u' : s_u , 'w_u' : w_u , 'pass_error' : pass_error , 'su_basic_sub' : su_basic_sub , 'su_user_sub' : su_user_sub , 'su_org_sub' : su_org_sub , 'su_store_sub' : su_store_sub}
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
        return redirect('index')
    else:
        organizations = get_user_organizations(user.id)
        
    
    context = {'organizations' : organizations}
    return render(request , 'galaxy/org_choose.html' , context)

def pricing(request):    
    switch_to_user_database('Users')
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # ---------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None
    
    try:
        admin_user = request.user.SubscriptionID.UserID
        su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
        su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
        su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
        su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
    except:
        pass
    
    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    p_ids = []
    if cart:
        for item in cart:
            p_ids.append(item.ProductID.id)
            
    sub_basic = Subscription.objects.filter(Bundle_T='Basic' , Status=True)
    cart_basic = Cart.objects.filter(Bundle_T='Basic')
    
    #------- for user profile form-------------------
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
    
    pass_error = []
    
    if request.method == 'POST':
        if 'save-profile' in request.POST:
            userform = ProfileForm(request.POST , request.FILES , instance=request.user)
            if userform.is_valid():
                userform.save()
                messages.success(request, "Profile saved successfully!")
    #-----------------------------------------------------------
    try:
        if request.user.user_Type == s_u or request.user.user_Type == w_u :
            messages.info(request , "• Due to your current user type you can only preview prices,if you want to buy create your own account.")
    except: 
        pass

        
    POS_M = Product.objects.get(id=6 , Type='Monthly')
    POS_A = Product.objects.get(id=2 , Type='Annually')
    IM_M = Product.objects.get(id=7 , Type='Monthly')
    IM_A = Product.objects.get(id=3 , Type='Annually')
    CRM_M = Product.objects.get(id=8 , Type='Monthly')
    CRM_A = Product.objects.get(id=4 , Type='Annually')
    A_M = Product.objects.get(id=9 , Type='Monthly')
    A_A = Product.objects.get(id=5 , Type='Annually')
    O_M = Product.objects.get(id=17 , Type='Monthly')
    O_A = Product.objects.get(id=10 , Type='Annually')
    STORE_M = Product.objects.get(id=18 , Type='Monthly') 
    STORE_A = Product.objects.get(id=11 , Type='Annually')
    U_M = Product.objects.get(id=19 , Type='Monthly')
    U_A = Product.objects.get(id=12 , Type='Annually')
    R_M = Product.objects.get(id=20 , Type='Monthly')
    R_A = Product.objects.get(id=13 , Type='Annually')
    T_M = Product.objects.get(id=21 , Type='Monthly')
    T_A = Product.objects.get(id=14 , Type='Annually')
    SLA_M = Product.objects.get(id=22 , Type='Monthly')
    SLA_A = Product.objects.get(id=15 , Type='Annually')
    STORAGE_M = Product.objects.get(id=23 , Type='Monthly')
    STORAGE_A = Product.objects.get(id=16 , Type='Annually')

    try:
        m_pos = Subscription.objects.filter( UserID=request.user , ProductID= POS_M)
    except:
        m_pos = None
    try:    
        a_pos = Subscription.objects.filter( UserID=request.user , ProductID= POS_A)
    except:
        a_pos = None
    try:    
        m_im = Subscription.objects.filter( UserID=request.user , ProductID= IM_M)
    except:
        m_im = None        
    try:
        a_im = Subscription.objects.filter( UserID=request.user , ProductID= IM_A)
    except:
        a_im = None   
    try:
        m_crm = Subscription.objects.filter( UserID=request.user , ProductID= CRM_M)
    except:
        m_crm = None   
    try:
        a_crm = Subscription.objects.filter( UserID=request.user , ProductID= CRM_A)
    except:
        a_crm = None    
    try:
        m_a = Subscription.objects.filter( UserID=request.user , ProductID= A_M)
    except:
        m_a = None   
    try:
        a_a = Subscription.objects.filter( UserID=request.user , ProductID= A_A)
    except:
        a_a = None  
    
    context = {'page_name' : 'Pricing' ,
               'POS_M' : POS_M ,
               'IM_M': IM_M ,
               'CRM_M' : CRM_M ,
               'A_M' : A_M ,
               'POS_A' : POS_A ,
               'IM_A' : IM_A ,
               'CRM_A' : CRM_A ,
               'A_A' : A_A ,
               'O_M' : O_M ,
               'O_A' : O_A ,
               'STORE_M' : STORE_M ,
               'STORE_A' : STORE_A ,
               'U_M' : U_M ,
               'U_A' : U_A ,
               'R_M' : R_M ,
               'R_A' : R_A ,
               'T_M' : T_M ,
               'T_A' : T_A , 
               'SLA_M' : SLA_M ,
               'SLA_A' : SLA_A ,
               'STORAGE_M' : STORAGE_M ,
               'STORAGE_A' : STORAGE_A,
               'in_cart' : in_cart ,
               'cart' : cart,
               'total' : total,
               'p_ids' : p_ids ,
               'm_pos' : m_pos,
               'a_pos' : a_pos,
               'm_im' : m_im,
               'a_im' : a_im,
               'm_crm' : m_crm,
               'a_crm' : a_crm,
               'm_a' : m_a,
               'a_a' : a_a,
               'cart_basic' : cart_basic,
               'sub_basic' : sub_basic,
               'userform' : userform ,
               's_a' : s_a ,
               's_u' : s_u ,
               'w_u' : w_u ,
               'pass_error' : pass_error ,
               'su_basic_sub' : su_basic_sub ,
               'su_user_sub' : su_user_sub ,
               'su_org_sub' : su_org_sub ,
               'su_store_sub' : su_store_sub
               }
    return render(request , 'galaxy/pricing.html' , context)


def add_cart(request , id , type , b_type):
    if not get_referer(request):
        raise Http404
    user = request.user
    try:
        product = Product.objects.get(id=id)
        obj_cart = Cart.objects.get(UserID=user , ProductID=product , Type=type , Bundle_T=b_type)
        obj_cart.Qty += 1
        obj_cart.save()
    except:
        product = Product.objects.get(id=id)
        obj_cart = Cart.objects.create(UserID=user , ProductID=product , Type=type , Qty=1 , Bundle_T=b_type)
        
    cart_items = Cart.objects.filter(UserID=request.user)
    sub_total = sum(item.ProductID.Price * item.Qty for item in cart_items)
    grand_total = sub_total
    
    response_data = {
        'success': True,
        'cart_items': list(cart_items.values()),  # Convert queryset to a list of dictionaries
        'subTotal': float(sub_total),
        'grandTotal': float(grand_total),
        'productName' : product.Name ,
        'quantity' : obj_cart.Qty ,
        'productPrice' : product.Price ,
        'productType' : product.Type ,
        'productId' : product.id ,
    }
    return JsonResponse(response_data)

def delete_cart(request , id):
    if not get_referer(request):
        raise Http404
    obj = Cart.objects.get(UserID=request.user , ProductID=id)
    if obj.Qty > 1:
        obj.Qty -= 1
        obj.save()
    else:
        obj.delete()
    
    cart_items = Cart.objects.filter(UserID=request.user)
    sub_total = sum(item.ProductID.Price * item.Qty for item in cart_items)
    grand_total = sub_total  # Add logic for applying any promotions or discounts
    
    # Prepare the JSON response
    response_data = {
        'success': True,
        'cart_items': list(cart_items.values()),  # Convert queryset to a list of dictionaries
        'subTotal': float(sub_total),
        'grandTotal': float(grand_total)
    }
    
    return JsonResponse(response_data)

def cart_total(request):
    total = 0
    item_in_cart = Cart.objects.filter(UserID=request.user)
    for item in item_in_cart:
        total += item.ProductID.Price * item.Qty
        
    # , id
@login_required
def payment(request):
    if not get_referer(request):
        raise Http404
    user = request.user
    current_date = datetime.now().date()
    end_date_m = current_date + timedelta(days=30)
    end_date_y = current_date + timedelta(days=365)
    # org_id = user.OrganizationID
    
    cart_items = Cart.objects.filter(UserID=user)
    if request.method == 'POST':
        if 'payment_btn' in request.POST:                                                            # if not create one
            for item in cart_items:
                if item.Type == 'Monthly' and item.Bundle_T == 'Basic':
                    for i in range(item.Qty):
                        Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_m , Type='Monthly' , Bundle_T='Basic')
                
                if item.Type == 'Monthly' and item.Bundle_T == 'Add-Ons':
                    for i in range(item.Qty):
                        sub=Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_m , Type='Monthly' , Bundle_T='Add-Ons')
                        if item.ProductID.Code == 201:
                            Organization.objects.create(UserID=user , SubscriptionID=sub , CreatedDate=current_date)
                            create_user_database('sub'+str(sub.id)+'_'+str(user.id))
                        if item.ProductID.Code == 203:
                            created_user = User.objects.create(SubscriptionID = sub , date_joined=current_date , Psw_Flag = 0)
                            created_user.Gender = 1
                            created_user.Language__id = 1
                            created_user.save()
                if item.Type == 'Annually' and item.Bundle_T == 'Basic':
                    for i in range(item.Qty):
                        Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_y , Type='Annually' , Bundle_T='Basic')
                
                if item.Type == 'Annually' and item.Bundle_T == 'Add-Ons':
                    for i in range(item.Qty):
                        sub=Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_y , Type='Annually' , Bundle_T='Add-Ons')
                        if item.ProductID.Code == 201:
                            Organization.objects.create(UserID=user , SubscriptionID=sub , CreatedDate=current_date)
                            create_user_database('sub'+str(sub.id)+'_'+str(user.id))
                        if item.ProductID.Code == 203:
                            created_user = User.objects.create(SubscriptionID = sub , date_joined=current_date , Psw_Flag = 0)
                            created_user.Gender = 1
                            created_user.Language__id = 1
                            created_user.save()
            # try:
            #     create_user_database(str(user.username)+'_'+str(user.id))
            # except:
            #     pass
            cart_items.delete()
            return redirect('success_m')
            
    context = {}
    return render(request , 'galaxy/payment.html' , context)

@login_required
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

@login_required
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
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # -------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None

    try:
        admin_user = request.user.SubscriptionID.UserID
        su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
        su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
        su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
        su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
    except:
        pass

    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
        
    #------- for user profile form-------------------
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
    
    pass_error = []
    
    if request.method == 'POST':
        if 'save-profile' in request.POST:
            userform = ProfileForm(request.POST , request.FILES , instance=request.user)
            if userform.is_valid():
                userform.save()
                messages.success(request, "Profile saved successfully!")
        elif 'contact-message' in request.POST:
            message = request.POST.get('Message')
            name = request.POST.get('Name')
            subject = request.POST.get('Subject')
            user_email = request.POST.get('Email')
            email=EmailMessage(
            f'{subject}',
            f'- Name : {name}\n\n- Email : {user_email}\n\n- Message : {message}',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            )
            email.fail_silently = False
            email.send()
            messages.success(request , "Email Sent!")
    #-----------------------------------------------------------
    
    context = {'page_name' : 'Contact-us' , 'subed' : subed , 'org' : org , 'in_cart' : in_cart , 'cart' : cart , 'total' : total , 'userform' : userform , 's_a' : s_a , 's_u' : s_u , 'w_u' : w_u , 'pass_error' : pass_error,  'su_basic_sub' : su_basic_sub , 'su_user_sub' : su_user_sub , 'su_org_sub' : su_org_sub , 'su_store_sub' : su_store_sub}
    return render(request , 'galaxy/contact.html' , context)

#--------------------------------------------------------------------------------
# def get_user_location(request):
#     # Get the user's IP address
#     user_ip = get_client_ip(request)
#     # Make a request to ipinfo.io to get location information
#     ipinfo_token = 'e2e096db330bce'  # Replace with your ipinfo.io token
#     api_url = f'https://ipinfo.io/{user_ip}?token={ipinfo_token}'

#     try:
#         response = requests.get(api_url)
#         data = response.json()

#         # Extract relevant information (you may adjust this based on ipinfo.io response structure)
#         city = data.get('city', 'N/A')
#         region = data.get('region', 'N/A')
#         country = data.get('country', 'N/A')

#         # Return the formatted location information
#         return f'{city}, {region}, {country}'
#     except Exception as e:
#         # Handle any errors (e.g., network issues, API rate limits)
#         print(f"Error getting location: {e}")
#         return 'N/A'
    
def get_user_location(request):
    # Get the user's IP address
    user_ip = get_client_ip(request)
    # user_ip = '197.53.227.100'
    # Make a request to ipinfo.io to get location information
    ipinfo_token = 'e2e096db330bce'  # Replace with your ipinfo.io token
    api_url = f'https://ipinfo.io/{user_ip}?token={ipinfo_token}'

    try:
        response = requests.get(api_url)
        data = response.json()

        # Extract latitude and longitude
        location = data.get('loc', 'N/A')

        # Return the formatted location information
        return location
    except Exception as e:
        # Handle any errors (e.g., network issues, API rate limits)
        print(f"Error getting location: {e}")
        return 'N/A'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_time_restrictions(user):
    try:
        current_time = datetime.now().time()
        current_day = datetime.now().strftime('%A')

        time_restrictions = user.timerestriction_set.filter(day_of_week=current_day)
        if time_restrictions.exists():
            for restriction in time_restrictions:
                try:
                    start_time = restriction.start_time
                    end_time = restriction.end_time
                    if start_time <= current_time < end_time:
                        return True
                except Exception as e:
                    print(f"An error occurred while comparing time values: {str(e)}")
                    return False
        else:
            # No time restrictions for the current day
            return True
      # return False
    except Exception as e:
        print(f"An error occurred while checking time restrictions: {str(e)}")
        return False

def login_page(request):
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    errors = []
    user_ip = get_client_ip(request)
    session_model = Session.objects.filter(expire_date__gte=timezone.now())
    users_logged = 1
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('psw')
        try:
            user = User.objects.get(email=email)
            allowed_ips = AllowedIp.objects.filter(UserId = user)
            try:    
                users_purchased = Subscription.objects.filter(UserID=user.SubscriptionID.UserID , ProductID__Code=203 , Status=True)
            except:
                pass
            if user.user_Type == s_a:
                if user.check_password(password):
                    login(request, user)
                    request.session['user_id'] = user.id
                    request.session['ip_address'] = get_client_ip(request)
                    request.session['location'] = get_user_location(request)
                    # Convert the time to the local timezone
                    local_time = timezone.localtime(timezone.now())
                    # Format the datetime
                    formatted_time = dateformat.format(local_time, 'Y-m-d H:i:s')
                    request.session['start_time'] = formatted_time
                    
                    messages.success(request , 'Logged in successfully!')
                    return redirect('index')
                else:
                    errors.append("Incorrect password!")
            else:
                if user.system_user_active:
                    if user.check_password(password):
                        if user.ip_restricted: 
                            if not allowed_ips:
                                errors.append("• Your ip address is not allowed to login to this user , please contact your admin!")
                                errors.append(f"• Your ip address ({user_ip})")
                            for ip in allowed_ips:
                                if ip.ip_address == user_ip:
                                    if check_time_restrictions(user):
                                        for session in session_model:
                                            session_data = session.get_decoded()
                                            if 'user_id' in session_data and session_data['user_id'] == user.id:
                                                users_logged += 1
                                        if users_logged > len(users_purchased):
                                            errors.append('• Another device already logged in to this user, please contact your admin for further info!')
                                        else:    
                                            login(request, user)
                                            request.session['user_id'] = user.id
                                            request.session['ip_address'] = get_client_ip(request)
                                            request.session['location'] = get_user_location(request)
                                            # Convert the time to the local timezone
                                            local_time = timezone.localtime(timezone.now())
                                            # Format the datetime
                                            formatted_time = dateformat.format(local_time, 'Y-m-d H:i:s')
                                            request.session['start_time'] = formatted_time
                                            if user.Psw_Flag == 1:
                                                messages.success(request , 'Logged in successfully!')
                                                return redirect('index')
                                            else:
                                                return redirect('pass_reset') # return for password page
                                    else:
                                        errors.append("You are not allowed to login at this time!")
                                else:
                                    errors.append("• Your ip address is not allowed to login to this user , please contact your admin!")
                                    errors.append(f"• Your ip address ({user_ip})")
                                    
                        else: 
                            if check_time_restrictions(user):
                                for session in session_model:
                                    session_data = session.get_decoded()
                                    if 'user_id' in session_data and session_data['user_id'] == user.id:
                                        users_logged += 1
                                if users_logged > len(users_purchased):
                                    errors.append('• Another device already logged in to this user, please contact your admin for further info!')
                                else:    
                                    login(request, user)
                                    request.session['user_id'] = user.id
                                    request.session['ip_address'] = get_client_ip(request)
                                    request.session['location'] = get_user_location(request)
                                    # Convert the time to the local timezone
                                    local_time = timezone.localtime(timezone.now())
                                    # Format the datetime
                                    formatted_time = dateformat.format(local_time, 'Y-m-d H:i:s')
                                    request.session['start_time'] = formatted_time
                                    if user.Psw_Flag == 1:
                                        messages.success(request , 'Logged in successfully!')
                                        return redirect('index')
                                    else:
                                        return redirect('pass_reset') # return for password page
                            else:
                                errors.append("You are not allowed to login at this time!")
                    else:
                        errors.append("Incorrect password!")
                else:
                     errors.append("your account is unactivated, contact your admin for more info!")       
        except :
            errors.append("Incorrect email address!")
    
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
        
        messages.success(request , 'your email is successfully activated, now you can login.')
        return redirect('activate_done') 
    else:
        messages.error(request , 'Activation link is invalid!')
    return redirect('index')   
    
    
    
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
        s_a = UsersType.objects.get(UserTypeCode='1')
        s_u = UsersType.objects.get(UserTypeCode='2')
        w_u = UsersType.objects.get(UserTypeCode='3')
        try:
            user = User.objects.get(email=email)
            errors.append('Email already associated with another account!')
        except:
            
            user = User.objects.create(email=email, username=username , user_Type = s_a , Psw_Flag=1)
            user.set_password(password)
            user.save()
            user.is_active = False
            user.save()
            active_email(request , user , email)
            # create the org for the user-----------------------------------------------------------------------------
            # org = Organization.objects.create(UserID=user , OrganizationName=organization , CreatedDate=current_date)
            # userr = User.objects.get(email = email)
            # userr.OrganizationID = org
            # userr.save()
            #-----------------------------------------------------------------------------------------------------------
             
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
            return redirect('activate_msg')
    else:
        errors = []

    context = {'errors': errors}
    return render(request, 'galaxy/register.html', context)


def signout(request):
   
    logout(request)
    messages.error(request , 'Logged out!')
    return redirect('index')

def activation_msg(request):
    context = {}
    return render(request , 'galaxy/activation_msg.html' , context)

def activation_done(request):
    if request.method == 'POST':
        return redirect('login')
    context = {}
    return render(request , 'galaxy/activation_done.html' , context)

@login_required
def my_products(request):
    if not get_referer(request):
        raise Http404
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # ------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None

    try:
        admin_user = request.user.SubscriptionID.UserID
        su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
        su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
        su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
        su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
    except:
        pass

    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    #------- for user profile form-------------------
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
        
    pass_error = []
    
    if request.method == 'POST':
        if 'save-profile' in request.POST:
            userform = ProfileForm(request.POST , request.FILES , instance=request.user)
            if userform.is_valid():
                userform.save()
                messages.success(request, "Profile saved successfully!")
    #-----------------------------------------------------------
    
    sub_basic = Subscription.objects.filter(UserID=request.user ,  Bundle_T='Basic')
    sub_add = Subscription.objects.filter(UserID=request.user, Bundle_T='Add-Ons').values('ProductID__Code', 'ProductID__Name').annotate(total_qty=Count('ProductID__Code'))
    userform = ProfileForm(instance=request.user)
    
    
    context = {'sub_basic' : sub_basic,'sub_add' : sub_add ,'in_cart' : in_cart , 'cart' : cart , 'total' : total , 'userform' : userform , 's_a' : s_a , 's_u' : s_u , 'w_u' : w_u , 'pass_error' : pass_error,  'su_basic_sub' : su_basic_sub , 'su_user_sub' : su_user_sub , 'su_org_sub' : su_org_sub , 'su_store_sub' : su_store_sub}
    return render(request , 'galaxy/my_products.html' , context)

@login_required      
def manage_org(request):
    if not get_referer(request):
        raise Http404
    
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # ------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None

    try:
        admin_user = request.user.SubscriptionID.UserID
        su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
        su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
        su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
        su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
    except:
        pass
    
    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    p_ids = []
    if cart:
        for item in cart:
            p_ids.append(item.ProductID.id)
    
    user = request.user
    org_subs = Subscription.objects.filter(UserID=user , ProductID__Code = 201)
    organisations = Organization.objects.filter(UserID = user)
    current_date = datetime.now().date()
    org = None
    try:
        choosed_org = request.GET.get('id')
    except:
        choosed_org = None
    try:
        org = Organization.objects.get(id=choosed_org)
    except:
        org = None
    try:
        sub_status = org.SubscriptionID.Status
        sub_start = org.SubscriptionID.StartDate
        sub_end = org.SubscriptionID.EndDate
        sub_autorenew = org.SubscriptionID.AutoRenew
    except:
        sub_status = None 
        sub_start = None  
        sub_end = None  
        sub_autorenew = None     
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
    try:
        sub_id = org.SubscriptionID.id
    except:
        sub_id = None
    #------------tax templates of an org-------------------------------------
    tax_temps = Taxes_Charges.objects.filter(org_id = choosed_org)
    #------------------------------------------------------------------------  
    # know the names of orgs of an user---------------------------------------
    # org_names = []
    orgs = Organization.objects.filter(UserID=request.user).exclude(id=choosed_org)

    # for org in orgs:
    #     if org.OrganizationName:
    #         org_names.append(org.OrganizationName)

        
    #------------------------------------------------------------------------------------
    form = OrgForm(instance=org)#, initial={'Currency': 1}
    #----------------------org tax form----------------------------------------------
    try:
        temp_id = request.GET.get('tempid')
        selected_temp = Taxes_Charges.objects.get(id=temp_id)
    except:
        temp_id = None
        selected_temp = None
        
    
    
    tax_form = OrgTax()
    #_-----------------------------------------------------------
    #-----------------------stores of a specific organization--------------------------------
    stores = Store.objects.filter(org_id = org)
    #-----------------------------------------------------------------------------------------
    #--------------get stores applied to a templates in a specifcic org ----------------------
    applied_stores = Store_Tax.objects.filter(org_id = org , tax_id = selected_temp)
    #-----------------------------------------------------------------------------------------
    #-------------------get departments and its categories-----------------------------------------
    departments = Department.objects.filter(org_id = org)
    
    # categories
    #--------------------------------------------------------------------------------------------
    try:
        form2 = AutoRenew(instance=org.SubscriptionID)
    except:
        form2 = None
        
    pass_error = []    
    del_btn = request.GET.get('del')

    if del_btn :
        code = secrets.token_hex(4)
        # Send the email with the code
        email=EmailMessage(
            'Organization Delete Confirmation',
            f'Your organization delete confirmation code is: {code}',
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently = False
        email.send()
        # Store the code in the session
        request.session['delete_code'] = code
        
    if request.method == 'POST':  
            # if 'save-btn' in request.POST:
            #     form = OrgForm(request.POST , request.FILES , instance=org)
            #     org_email = request.POST.get('OrganizationEmail')
            #     org_username = request.POST.get('OrganizationName')
            #     org_cost_method = request.POST.get('Cost_Method')
                
            #     if form.is_valid():
            #         if not org_email:
            #             messages.error(request,'• Organization Email Required')
            #         if not org_username:
            #             messages.error(request,'• Organization Username Required')
            #         if any(org_username.lower() == name.OrganizationName.lower() for name in orgs):
            #             messages.error(request,'• already using this organization name!')
            #             url = f'/my_products/organizations?id={choosed_org}'
            #             return redirect(url)
            #         if not org_cost_method:
            #             messages.error(request,'• Organization Cost Method Required')  
            #         if org_email and org_username and org_cost_method and any(org_username.lower() != name.OrganizationName.lower() for name in orgs):
            #             messages.success(request,'Organization Saved Successfully!')
            #             org=form.save()

            #     else:
            #         # Form is not valid, handle errors
            #         for field, errors in form.errors.items():
            #             for error in errors:
            #                 if error == "Organization with this OrganizationEmail already exists.":
            #                     messages.error(request, '• Organization email already exists!')
                    
            #         url = f'/my_products/organizations?id={choosed_org}'
            #         return redirect(url)
   
            if 'Auto-Renew' in request.POST:
                
                form2 = AutoRenew(request.POST , instance=org.SubscriptionID)
                value = request.POST.get('Auto-Renew')
                if value == 'on':
                    auto_value = "True"
                else:
                    auto_value = "False"
                   
                org = Organization.objects.get(id = choosed_org)
                subs = org.SubscriptionID
                subs.AutoRenew = auto_value
                subs.save()
                form2 = AutoRenew(instance=subs)
            elif 'save-profile' in request.POST:
                userform = ProfileForm(request.POST , request.FILES , instance=request.user)
                if userform.is_valid():
                    userform.save() 
                    messages.success(request, "Profile saved successfully!")

            
    userform = ProfileForm(instance=request.user)       
   
    context = {'organisations' : organisations ,
               'form' : form ,
               'sub_status' : sub_status ,
               'sub_start' : sub_start ,
               'sub_end' : sub_end ,
               'sub_autorenew' : sub_autorenew ,
               'form2' : form2 ,
               'choosed_org' : choosed_org ,
               'org_subs' : org_subs ,
               'in_cart' : in_cart,
               'total' : total,
               'org' : org ,
               'userform' : userform ,
               'cart' : cart , 
               's_a' : s_a ,
               's_u' : s_u ,
               'w_u' : w_u ,
               'pass_error' : pass_error ,
               'su_basic_sub' : su_basic_sub ,
               'su_user_sub' : su_user_sub ,
               'su_org_sub' : su_org_sub ,
               'su_store_sub' : su_store_sub ,
               'tax_temps' : tax_temps ,
               'tax_form' : tax_form , 
               'stores' : stores , 
               'applied_stores' : applied_stores,
               'departments' : departments,
               }
    
    
    return render(request , 'galaxy/manage_org.html' , context)

def delete_org(request , id):
        if not get_referer(request):
            raise Http404
        user = request.user
        # Get the code entered by the user
        user_code = request.GET.get('code')

        # Get the code stored in the session
        stored_code = request.session.get('delete_code')

        if user_code == stored_code:
            org_id = id
            organisation = Organization.objects.get(id=org_id)
            sub_id = organisation.SubscriptionID.id
            organisation.OrganizationName = None
            organisation.Com_Regm = None
            organisation.Tax_Reg = None
            organisation.Logo = None
            organisation.Report_B = None
            organisation.Report_H = None
            organisation.Address = None
            organisation.Country = None
            organisation.Currency = None
            organisation.Cost_Method = None
            organisation.Create_Receive = False
            organisation.Create_Issue = False
            organisation.Terms = None
            organisation.OrganizationEmail = None
            organisation.WebsiteLink = None
            organisation.WhatsappLink = None
            organisation.FacebookLink = None
            organisation.InstgramLink = None
            organisation.save()
            # Delete the stored code from the session
            # del request.session['delete_code']
            db_name = f'sub{sub_id}_{request.user.id}'
            delete_user_database(db_name)
            create_user_database(db_name)
            # Redirect the user to a success page
            messages.success(request , 'Organization Deleted Successfully!')
            response_data = {
                'success': True,
                'message' : 'Organization Deleted Successfully'
            }
            # Delete the stored code from the session
            # del request.session['delete_code']
            # Redirect the user to a success page
        else:
            response_data = {
                'error': True ,
            }
            
    
        
        
        return JsonResponse(response_data)

@login_required
def manage_user(request):
    if not get_referer(request):
        raise Http404
    
    s_a = UsersType.objects.get(UserTypeCode='1')
    s_u = UsersType.objects.get(UserTypeCode='2')
    w_u = UsersType.objects.get(UserTypeCode='3')
    # ------------------------------------------------------------------
    su_basic_sub = None
    su_user_sub = None
    su_org_sub = None
    su_store_sub = None
    
    try:
        admin_user = request.user.SubscriptionID.UserID
        su_basic_sub = Subscription.objects.filter(Bundle_T='Basic', UserID=admin_user)
        su_user_sub = Subscription.objects.filter(ProductID__Code = 203, UserID=admin_user)
        su_org_sub = Subscription.objects.filter(ProductID__Code = 201, UserID=admin_user)
        su_store_sub = Subscription.objects.filter(ProductID__Code = 202, UserID=admin_user)
    except:
        pass

    # for total price in cart -----------------------------------------
    total = 0
    try:
        item_in_cart = Cart.objects.filter(UserID=request.user)
    except:
        item_in_cart = None
    if item_in_cart: 
        for item in item_in_cart:
            total += item.ProductID.Price * item.Qty
    # for number of object in cart -------------------------------------
    in_cart = 0
    
    try:
        cart = Cart.objects.filter(UserID=request.user)
    except:
        cart = None
    if cart:
        for p in cart:
            in_cart += 1 * p.Qty
    p_ids = []
    if cart:
        for item in cart:
            p_ids.append(item.ProductID.id)
    
    user = request.user
    try:
        user_subs_basic = Subscription.objects.filter(UserID = user , Bundle_T = 'Basic')
    except:
        user_subs_basic = None
    try:
        users = User.objects.filter(SubscriptionID__UserID = user)
    except:
        users = None
    current_date = datetime.now().date()
    # the_user = None
    try:
        choosed_user = request.GET.get('id')
    except:
        choosed_user = None
    try:
        the_user = User.objects.get(id=choosed_user)
    except:
        the_user = None
    try:
        sub_status = the_user.SubscriptionID.Status
        sub_start = the_user.SubscriptionID.StartDate
        sub_end = the_user.SubscriptionID.EndDate
        sub_autorenew = the_user.SubscriptionID.AutoRenew
    except:
        sub_status = None 
        sub_start = None  
        sub_end = None  
        sub_autorenew = None     
    try:
        userform = ProfileForm(instance=request.user)
    except:
        userform = None
    try:
        sub_id = the_user.SubscriptionID.id
    except:
        sub_id = None
    try:
        form = SystemUserForm(user_id=the_user.id, instance=the_user)
    except:
        form = None
         
    try:
        form2 = AutoRenew(instance=the_user.SubscriptionID)
    except:
        form2 = None
    
    try:
        user_module = AllowedModule.objects.filter(UserId = the_user)
    except:
        user_module = None
    try:
        ip_addresses = AllowedIp.objects.filter(UserId = the_user)
    except:
        ip_addresses = None
    
    
# ---------------to know if there are session with specific user------------------
    try:
        session_model = Session.objects.filter(expire_date__gte=timezone.now())
        the_user_sessions = []
        the_user_sessions_info = []

        for session in session_model:
            session_data = session.get_decoded()
            if 'user_id' in session_data and session_data['user_id'] == the_user.id:
                ip_address = session_data.get('ip_address', 'N/A')
                location = session_data.get('location', 'N/A')
                start_time = session_data.get('start_time')
                session_store = SessionStore(session_key=session.session_key)
                the_user_sessions.append(session_store)

                print('Session Data:', session_data)
                session_info = {
                    'session_id': session.session_key,
                    'ip_address': ip_address,
                    'location': location,
                    'start_time': start_time,
                }
                the_user_sessions_info.append(session_info)
                print(the_user_sessions_info)
    except:
        print('passed')
# --------------------------------------------------------------------------------------------
    time_restrictions = TimeRestriction.objects.filter(UserID=the_user)

    # time_restrictions_dict = {}
    # for restriction in time_restrictions:
    #     time_restrictions_dict[restriction.day_of_week] = [restriction.start_time, restriction.end_time]


    pass_error_user=[]
    
    pass_error= []
    
    del_btn = request.GET.get('del')
    if del_btn :
            code = secrets.token_hex(4)
            # Send the email with the code
            email=EmailMessage(
                'User Delete Confirmation',
                f'Your user delete confirmation code is: {code}',
                settings.EMAIL_HOST_USER,
                [request.user.email],
            )
            email.fail_silently = False
            email.send()
            # Store the code in the session
            request.session['delete_code'] = code
                
            # response_data = {
            #     'success': True,
            #     'id' : choosed_user ,
            #     }
    
            # return JsonResponse(response_data)
    
    if request.method == 'POST':
        # if 'user-save-btn' in request.POST:
            
        #     form = SystemUserForm(request.POST  or None, request.FILES  or None, user_id=the_user.id, instance=the_user , initial={'Gender': 1, 'Language': 1})
        #     password = request.POST.get('password')
        #     password2 = request.POST.get('psw-repeat')
        #     email = request.POST.get('email')
            
        #     if form.is_valid():
        #         if password:
        #             if check_password(password, the_user.password):
        #                 messages.error(request, '• Can\'t use the same old password!')
        #                 pass_error_user.append('• Can\'t use the same old password!') 
        #             elif password == password2 and len(password) > 8 and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        #                 the_user = form.save(commit = False)
        #                 the_user.Psw_Flag = 0
        #                 the_user.save()
                        
        #                 session_model = Session.objects.filter(expire_date__gte=timezone.now())
        #                 sessions_with_value = []

        #                 for session in session_model:
        #                     session_data = session.get_decoded()
        #                     if 'user_id' in session_data and session_data['user_id'] == the_user.id:
        #                         session_store = SessionStore(session_key=session.session_key)
        #                         sessions_with_value.append(session_store)
        #                         print(sessions_with_value)
        #                 for session_store in sessions_with_value:
        #                     session_store.delete() 
                        
        #                 messages.success(request, 'User saved successfully!')
        #                 if password and email:
        #                     email_msg=EmailMessage(
        #                     'Galaxy ERP account',
        #                     f'Your login info, Email:{email} & Password:{password}',
        #                     settings.EMAIL_HOST_USER,
        #                     [email],
        #                     )
        #                     email_msg.fail_silently = False
        #                     email_msg.send()
        #                     url = f'/my_products/users?id={choosed_user}'
        #                     return redirect(url)
        #             else:
        #                 messages.error(request, '• Couldn\'t save User, Password error!')
        #                 if len(password) < 8:
                
        #                     form = SystemUserForm(request.POST  or None, request.FILES  or None, user_id=the_user.id, instance=the_user , initial={'Gender': 1, 'Language': 1})
        #                     pass_error_user.append('• Passwords is less than 8 Characters!')
        #                 # Check if password contains a number
        #                 if not re.search(r'\d', password):
                        
        #                     form = SystemUserForm(request.POST  or None, request.FILES  or None, user_id=the_user.id, instance=the_user, initial={'Gender': 1, 'Language': 1})
        #                     pass_error_user.append('• Passwords doesn\'t contain numbers!')
                        
        #                 # Check if password contains a special character
        #                 if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                        
        #                     form = SystemUserForm(request.POST  or None, request.FILES  or None, user_id=the_user.id, instance=the_user, initial={'Gender': 1, 'Language': 1})
        #                     pass_error_user.append('• Passwords doesn\'t contain special character!')
                        
        #                 # Check if password contains lowercase letters
        #                 if not re.search(r'[a-z]', password):
                        
        #                     form = SystemUserForm(request.POST  or None, request.FILES  or None, user_id=the_user.id, instance=the_user, initial={'Gender': 1, 'Language': 1})
        #                     pass_error_user.append('• Passwords doesn\'t contain lower letter!')
                        
        #                 # Check if password contains uppercase letters
        #                 if not re.search(r'[A-Z]', password):
                            
        #                     form = SystemUserForm(request.POST or None, request.FILES  or None, user_id=the_user.id, instance=the_user, initial={'Gender': 1, 'Language': 1})
        #                     pass_error_user.append('• Passwords doesn\'t contain upper letter!')
                        
                        
        #                 if password != password2:
                            
        #                     form = SystemUserForm(request.POST  or None, request.FILES  or None, user_id=the_user.id, instance=the_user, initial={'Gender': 1, 'Language': 1})
        #                     pass_error_user.append('• Passwords Didn\'t Match!')
                                
        #         else:  
        #             the_user = form.save()
        #             messages.success(request, 'User saved successfully!')
        #             url = f'/my_products/users?id={choosed_user}'
        #             return redirect(url)
        #     if not form.is_valid():
        #         for field, errors in form.errors.items():
        #             if field != 'password': 
        #                 for error in errors:
        #                     messages.error(request,f"• {error}" )
        #         form = SystemUserForm(request.POST or None, request.FILES  or None, user_id=the_user.id , instance=the_user, initial={'Gender': 1 , 'Language': 1})   
            
        if 'save-profile' in request.POST:
            userform = ProfileForm(request.POST , request.FILES , instance=request.user)
            if userform.is_valid():
                userform.save()  
                messages.success(request, "Profile saved successfully!") 
    
    
    
    
    
            
               
    context = {'users' : users ,
               'form' : form ,
               'sub_status' : sub_status ,
               'sub_start' : sub_start ,
               'sub_end' : sub_end ,
               'sub_autorenew' : sub_autorenew ,
               'form2' : form2 ,
               'choosed_user' : choosed_user ,
               'user_subs_basic' : user_subs_basic ,
               'in_cart' : in_cart,
               'total' : total,
               'the_user' : the_user ,
               'userform' : userform ,
               'cart' : cart ,
               's_a' : s_a ,
               's_u' : s_u ,
               'w_u' : w_u ,
               'pass_error' : pass_error ,
               'pass_error_user' : pass_error_user ,
               'user_module' : user_module ,
               'ip_addresses' : ip_addresses , 
            #    'time_restrictions': time_restrictions_dict ,
               'su_basic_sub' : su_basic_sub ,
               'su_user_sub' : su_user_sub ,
               'su_org_sub' : su_org_sub ,
               'su_store_sub' : su_store_sub,
               'the_user_sessions' : the_user_sessions,
               'time_restrictions' : time_restrictions,
               'the_user_sessions_info' : the_user_sessions_info
               }
    return render(request , 'galaxy/manage_user.html' , context)


def delete_user(request , id):
        if not get_referer(request):
            raise Http404
        # Get the code entered by the user      
        user_code = request.GET.get('code')
        # Get the code stored in the session
        stored_code = request.session.get('delete_code')
        if user_code == stored_code:
            user_id = id
            user = User.objects.get(id=user_id)
            user.username = None
            user.email = None
            user.first_name = None
            user.last_name = None
            user.avatar = None
            user.user_Type = None
            user.Language = None
            user.Birth_Date = None
            user.Gender = None
            user.Telephone = None
            user.password = None
            user.is_active = True
            user.save()
            messages.success(request , 'User Deleted Successfully!')
            response_data = {
                'success': True,
            }
            # Delete the stored code from the session
            # del request.session['delete_code']
            # Redirect the user to a success page
        else:
            response_data = {
                'error': True ,
                'message' : 'User Deleted Successfully!'
            }
            
    
        
        
        return JsonResponse(response_data)

def pass_reset(request):
    if not get_referer(request):
        raise Http404
    current_password = request.POST.get('currentpsw')
    password = request.POST.get('psw')
    password2 = request.POST.get('psw-repeat')
    pass_error = []
    
    if request.method == 'POST':
        if check_password(current_password, request.user.password):
            if password:
                if password == password2 and password != current_password and len(password) > 8 and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
                    request.user.set_password(password) 
                    request.user.Psw_Flag = 1
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Password Updated Successfully!')
                    return redirect('index')
                    
                elif password == current_password:
                    messages.error(request, '• Can\'t Use The Same Old Password!')
                    
                
                else:
                    
                    messages.error(request, '• Couldn\'t Save Password!')
                    if len(password) < 8:
                        pass_error.append('• Password is less than 8 Characters!')
                    
                    # Check if password contains a number
                    if not re.search(r'\d', password):
                        pass_error.append('• Password doesn\'t contain numbers!')
                    
                    # Check if password contains a special character
                    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                        pass_error.append('• Password doesn\'t contain special character!')
                    
                    # Check if password contains lowercase letters
                    if not re.search(r'[a-z]', password):
                        pass_error.append('• Password doesn\'t contain lower letter!')
                    
                    # Check if password contains uppercase letters
                    if not re.search(r'[A-Z]', password):
                        pass_error.append('• Password doesn\'t contain upper letter!')
                    
                    
                    if password != password2:
                        pass_error.append('• Passwords Didn\'t Match!')
            
            else:
                messages.error(request , 'Add New Password!')
                
        else:
            messages.error(request , 'Current Password Is Invalid!')


    
    context={'pass_error' : pass_error}
    return render(request , 'galaxy/user_pass_reset.html' , context)



def applying_promocode(request , code , total):
    
    try:
        promotion = PromoCode.objects.get(code=code)
        
        if promotion.usercode :
            if promotion.usercode == request.user:
                if promotion.code == code and promotion.status == True:
                    grandtotal = total-((promotion.discount/100)*total)
                    response_data = {
                    'success': True,
                    'grandtotal' : grandtotal,
                    
                    }
                elif promotion.code != code:
                    response_data = {
                'error': True,
                }
                    
                elif promotion.status == False and promotion.code == code:
                    response_data = {
                'expired': True,
                }
            elif promotion.usercode != request.user:
                response_data = {
            'error': True,
            }
        else:
            if promotion.code == code and promotion.status == True:
                    grandtotal = total-((promotion.discount/100)*total)
                    response_data = {
                    'success': True,
                    'grandtotal' : grandtotal,
                    
                    }
            elif promotion.code != code:
                    response_data = {
                'error': True,
                }
                    
            elif promotion.status == False and promotion.code == code:
                    response_data = {
                'expired': True,
                }
    except:
        response_data = {
        'error': True,
        }
    
    return JsonResponse(response_data)


def pass_change(request):
            if not get_referer(request):
                raise Http404
            pass_error = []
            current_password = request.GET.get('cpsw') 
            password = request.GET.get('npsw')  
            password2 = request.GET.get('rpsw') 
            
            if check_password(current_password, request.user.password):
                if password:
                    if password == password2 and password != current_password and len(password) > 8 and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
                        request.user.set_password(password) 
                        request.user.save()
                        update_session_auth_hash(request, request.user)
                        
                        # current_url = request.build_absolute_uri()
                        # redirect_url = f"{current_url}?auto_open=true"
                        # return redirect(redirect_url)
                        response_data = {
                            'success': True,
                            'message' : 'Password Updated Successfully!'
                        }
                        
                        
                    elif password == current_password:
                        
                        # current_url = request.build_absolute_uri()
                        # redirect_url = f"{current_url}?auto_open=true"
                        # return redirect(redirect_url)
                        response_data = {
                            'samePswError': True,
                            'message' : '• Can\'t Use The Same Old Password!'
                        }
                    
                    else:  
                        if len(password) < 8:
                            pass_error.append('• Password is less than 8 Characters!')
                        
                        # Check if password contains a number
                        if not re.search(r'\d', password):
                            pass_error.append('• Password doesn\'t contain numbers!')
                        
                        # Check if password contains a special character
                        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                            pass_error.append('• Password doesn\'t contain special character!')
                        
                        # Check if password contains lowercase letters
                        if not re.search(r'[a-z]', password):
                            pass_error.append('• Password doesn\'t contain lower letter!')
                        
                        # Check if password contains uppercase letters
                        if not re.search(r'[A-Z]', password):
                            pass_error.append('• Password doesn\'t contain upper letter!')
                        
                        
                        if password != password2:
                            pass_error.append('• Passwords Didn\'t Match!')
                        
                        response_data = {
                            'pswError': True,
                            'pass_error' : pass_error,
                            'message' : '• Couldn\'t Save Password!'
                        }           
                        # current_url = request.build_absolute_uri()
                        # redirect_url = f"{current_url}?auto_open=true"
                        # return redirect(redirect_url)
            
                else:
                    
                    response_data = {
                            'noPassError': True,
                            'message' : '• Add New Password!'
                        }     
                
            else:
                # current_url = request.build_absolute_uri()
                # redirect_url = f"{current_url}?auto_open=true"
                # return redirect(redirect_url)
                
                response_data = {
                    'cPswError': True,
                    'message' : '• Current Password Is Invalid!'
                }
    
            return JsonResponse(response_data)
        
        
        
        
def add_allow_module(request):
 
    id = request.GET.get('id')
    user = User.objects.get(id = id)
    module_name = request.GET.get('module_name')
    module = Product.objects.get(Name = module_name , Type = 'Monthly')
    adding_module = AllowedModule.objects.create(UserId = user , module_code = module.Code , module_name = module_name)
 
    response_data = {
                    'success': True,
                    'message' : 'Module Added!'
                }
    
    return JsonResponse(response_data)

def delete_allow_module(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id = id)
    module_name = request.GET.get('module_name')
    module = Product.objects.get(Name = module_name , Type = 'Monthly')
    user_module = AllowedModule.objects.get(UserId = user , module_code = module.Code , module_name = module_name)
    user_module.delete()
    
    
    response_data = {
                    'success': True,
                    'message' : 'Module Removed!'
                }
  
    return JsonResponse(response_data)


def add_allow_ip(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id = id)
    ip_address = request.GET.get('ip_address')
    adding_address = AllowedIp.objects.create(UserId = user , ip_address = ip_address)
 
    response_data = {
                    'success': True,
                    'message' : 'IP Address Added!'
                }
  
    return JsonResponse(response_data)


def delete_allow_ip(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id = id)
    ip_address = request.GET.get('ip_address')
    user_ip = AllowedIp.objects.get(UserId = user , ip_address = ip_address)
    user_ip.delete()
    
    
    response_data = {
                    'success': True,
                    'message' : 'IP Address Removed!'
                }
  
    return JsonResponse(response_data)


def allow_all_ip(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id=id)
    user.ip_restricted = False
    user.save()
    
    response_data = {
                    'success': True,
                    'message' : 'All IPs Allowed!'
                }
  
    return JsonResponse(response_data)


def restrict_ip(request):
    
    access_users = AllowedIp.objects.filter(UserId=request.user)
    user_id = request.GET.get('id')
    user = User.objects.get(id=user_id)
    user.ip_restricted = True
    user.save()


    # session_model = Session.objects.filter(expire_date__gte=timezone.now())
    # sessions_with_value = []

    # for session in session_model:
    #     session_data = session.get_decoded()
    #     if 'user_id' in session_data and session_data['user_id'] == user.id:
    #         session_store = SessionStore(session_key=session.session_key)
    #         sessions_with_value.append(session_store)
    #         print(sessions_with_value)
    # for session_store in sessions_with_value:
        
    #     session_store.delete() 

    response_data = {
        'success': True,
        'message': 'Login IP Restricted!'
    }

    return JsonResponse(response_data)

def user_renew_on(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id=id)
    user.SubscriptionID.AutoRenew = True    
    user.SubscriptionID.save()
    
    response_data = {
                    'success': True,
                    'message' : 'Auto Renew ON!'
                }
  
    return JsonResponse(response_data)

def user_renew_off(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id=id)
    user.SubscriptionID.AutoRenew = False
    user.SubscriptionID.save()
    
    response_data = {
                    'success': True,
                    'message' : 'Auto Renew OFF!'
                }
  
    return JsonResponse(response_data)

def org_renew_on(request):
    
    id = request.GET.get('id')
    org = Organization.objects.get(id=id)
    org.SubscriptionID.AutoRenew = True
    org.SubscriptionID.save()
    
    response_data = {
                    'success': True,
                    'message' : 'Auto Renew ON!'
                }
  
    return JsonResponse(response_data)

def org_renew_off(request):
    id = request.GET.get('id')
    org = Organization.objects.get(id=id)
    org.SubscriptionID.AutoRenew = False
    org.SubscriptionID.save()
    
    response_data = {
                    'success': True,
                    'message' : 'Auto Renew OFF!'
                }
  
    return JsonResponse(response_data)


def time_restrictions(request, user_id, day, start, end):
    
    user = User.objects.get(id=user_id)
    day_of_week=  day
    start_time = start
    end_time = end
    try:
        day_access = TimeRestriction.objects.get(UserID=user , day_of_week=day_of_week)
    except:
        day_access = None
    
    if day_access:
        
        day_access.start_time = start
        day_access.end_time = end
        day_access.save()
    else:
        
        time_restriction = TimeRestriction.objects.create(UserID=user, day_of_week=day_of_week, start_time=start, end_time=end)

    # session_model = Session.objects.filter(expire_date__gte=timezone.now())
    # sessions_with_value = []

    # for session in session_model:
    #     session_data = session.get_decoded()
    #     if 'user_id' in session_data and session_data['user_id'] == user.id:
    #         session_store = SessionStore(session_key=session.session_key)
    #         sessions_with_value.append(session_store)
    #         print(sessions_with_value)
    # for session_store in sessions_with_value:
    #     session_store.delete()   
        
    response_data = {
            'success': True,
            'message' : 'Access time saved!'
        }
    
    return JsonResponse(response_data)    
    

def remove_time_restrictions(request):
    
    id = request.GET.get('id')
    user = User.objects.get(id=id)
    day = request.GET.get('day')
    
    time_restriction = TimeRestriction.objects.get(UserID=user , day_of_week = day)
    time_restriction.delete()
        
    response_data = {
            'success': True,
            'message' : 'Time restriction removed!'
        } 
    
    return JsonResponse(response_data)

def save_system_user(request, userid):
    response_data = {}

    if request.method == 'POST':
        # If using AJAX, get data from POST directly

        the_user = User.objects.get(id=userid)
        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)#, initial={'Gender': 1, 'Language': 1}
        password = request.POST.get('password')
        password2 = request.POST.get('psw-repeat')
        email = request.POST.get('email')
        telephone = request.POST.get('Telephone')
        
        if form.is_valid():
            if password and the_user.password:
                if check_password(password, the_user.password):
                    # messages.error(request, '• Can\'t use the same old password!')
                    response_data = {
                        'error': True,
                        'message': '• Can\'t use the same old password!'
                    }
                elif password == password2 and len(password) > 8 and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
                    the_user = form.save(commit=False)
                    the_user.Psw_Flag = 0
                    the_user.save()

                    session_model = Session.objects.filter(expire_date__gte=timezone.now())
                    sessions_with_value = []

                    for session in session_model:
                        session_data = session.get_decoded()
                        if 'user_id' in session_data and session_data['user_id'] == the_user.id:
                            session_store = SessionStore(session_key=session.session_key)
                            sessions_with_value.append(session_store)

                    for session_store in sessions_with_value:
                        session_store.delete()

                    # messages.success(request, 'User saved successfully!')
                    if password and email:
                        email_msg = EmailMessage(
                            'Galaxy ERP account',
                            f'Your login info, Email:{email} & Password:{password}',
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                        email_msg.fail_silently = False
                        email_msg.send()

                    response_data = {
                        'success': True,
                        'message': 'User saved successfully!'
                    }
                else:

                    if len(password) < 8:
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords is less than 8 Characters!'
                        }

                    # Check if password contains a number
                    if not re.search(r'\d', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain numbers!'
                        }

                    # Check if password contains a special character
                    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain special character!'
                        }

                    # Check if password contains lowercase letters
                    if not re.search(r'[a-z]', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain lower letter!'
                        }

                    # Check if password contains uppercase letters
                    if not re.search(r'[A-Z]', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain upper letter!'
                        }

                    if password != password2:
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords Didn\'t Match!'
                        }
            elif password and not the_user.password:
                if password == password2 and len(password) > 8 and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
                    the_user = form.save(commit=False)
                    the_user.Psw_Flag = 0
                    the_user.save()

                    session_model = Session.objects.filter(expire_date__gte=timezone.now())
                    sessions_with_value = []

                    for session in session_model:
                        session_data = session.get_decoded()
                        if 'user_id' in session_data and session_data['user_id'] == the_user.id:
                            session_store = SessionStore(session_key=session.session_key)
                            sessions_with_value.append(session_store)

                    for session_store in sessions_with_value:
                        session_store.delete()

                    # messages.success(request, 'User saved successfully!')
                    if password and email:
                        email_msg = EmailMessage(
                            'Galaxy ERP account',
                            f'Your login info, Email:{email} & Password:{password}',
                            settings.EMAIL_HOST_USER,
                            [email],
                        )
                        email_msg.fail_silently = False
                        email_msg.send()

                    response_data = {
                        'success': True,
                        'message': 'User saved successfully!'
                    }
                else:

                    if len(password) < 8:
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords is less than 8 Characters!'
                        }

                    # Check if password contains a number
                    if not re.search(r'\d', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain numbers!'
                        }

                    # Check if password contains a special character
                    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain special character!'
                        }

                    # Check if password contains lowercase letters
                    if not re.search(r'[a-z]', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain lower letter!'
                        }

                    # Check if password contains uppercase letters
                    if not re.search(r'[A-Z]', password):
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords doesn\'t contain upper letter!'
                        }

                    if password != password2:
                        form = SystemUserForm(request.POST or None, request.FILES or None, user_id=the_user.id, instance=the_user)
                        response_data = {
                            'error': True,
                            'message': '• Passwords Didn\'t Match!'
                        }
            else:
                if telephone:
                    phone_number = phonenumbers.parse(telephone, "US")

                    # Check if the phone number is valid
                    is_valid = phonenumbers.is_valid_number(phone_number)

                    # Get the formatted international phone number
                    formatted_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                    print(formatted_number)
                    if is_valid:
                        the_user = form.save()
                        response_data = {
                            'success': True,
                            'message': '• User saved successfully!'
                        }
                    else:
                        response_data = {
                            'error': True,
                            'message': '• Telephone number is invalid!'
                        }
        else:
            print('ok')
            form_errors = []
            for field, errors in form.errors.items():
                if field == "email":
                    response_data = {
                        'error': True,
                        'message': "• Email already exists"
                    }
                elif field == "Telephone":
                    response_data = {
                        'error': True,
                        'message': "• Telephone number already exists"
                    }
                
                    

    return JsonResponse(response_data)

def save_org(request, orgid):
    response_data = {}
    org = Organization.objects.get(id=orgid)
    orgs = Organization.objects.filter(UserID=request.user).exclude(id=orgid)
    if request.method == 'POST':
        form = OrgForm(request.POST , request.FILES , instance=org)
        org_email = request.POST.get('OrganizationEmail')
        org_username = request.POST.get('OrganizationName')
        org_cost_method = request.POST.get('Cost_Method')
        
        if form.is_valid():
            if not org_email:
                # messages.error(request,'• Organization Email Required')
                response_data = {
                    'error': True,
                    'message': '• Organization Email Required',
                }
            if not org_username:
                # messages.error(request,'• Organization Username Required')
                response_data = {
                    'error': True,
                    'message': '• Organization Username Required',
                }
            if any(org_username.lower() == name.OrganizationName.lower() for name in orgs):
                # messages.error(request,'• already using this organization name!')
                response_data = {
                    'error': True,
                    'message': '• already using this organization name!',
                }
            if not org_cost_method:
                # messages.error(request,'• Organization Cost Method Required')  
                response_data = {
                    'error': True,
                    'message': '• Organization Cost Method Required',
                }
            if org_email and org_username and org_cost_method and any(org_username.lower() != name.OrganizationName.lower() for name in orgs):
                # messages.success(request,'Organization Saved Successfully!')
                org=form.save()
                response_data = {
                    'success': True,
                    'message': '• Organization Saved Successfully!',
                }

        else:
            # Form is not valid, handle errors
            for field, errors in form.errors.items():
                for error in errors:
                    if error == "Organization with this OrganizationEmail already exists.":
                        # messages.error(request, '• Organization email already exists!')
                        response_data = {
                            'error': True,
                            'message': '• Organization email already exists!',
                        }

    return JsonResponse(response_data)


def session_del(request, session_id):

    session_model = Session.objects.filter(expire_date__gte=timezone.now())
    sessions_with_value = []

    for session in session_model:
        session_data = session.get_decoded()
        print("session_data")
        if session.session_key == session_id:
           session.delete()
           break
    
    response_data = {
                    'success': True,
                    'message': '• Session deleted',
                    }
    return JsonResponse(response_data)


def get_tax_data(request, temp_id):
    try:
        selected_temp = Taxes_Charges.objects.get(id=temp_id)
        # tax_form = OrgTax(instance=selected_temp)
        store_taxes = Store_Tax.objects.filter(tax_id = selected_temp)
        linked_stores = []
        form_data = {
            'tax_title': selected_temp.tax_title, #tax_form['tax_title'].value()
            'tax_include': selected_temp.tax_include, #tax_form['tax_include'].value()
            'default': selected_temp.default, #tax_form['default'].value()
            'disable': selected_temp.disable, #tax_form['disable'].value()
            'min_amount': selected_temp.min_amount, #tax_form['min_amount'].value()
            'max_amount': selected_temp.max_amount, #tax_form['max_amount'].value()
            'tax_type': selected_temp.tax_type, #tax_form['tax_type'].value()
            'tax_amount': selected_temp.tax_amount, #tax_form['tax_amount'].value()
            'rate': selected_temp.rate, #tax_form['rate'].value()
            'amount': selected_temp.amount, #tax_form['amount'].value()
            # Add other fields as needed
        }
        for store in store_taxes:
            info = {
                'name' : store.store_id.name,
                'id' : store.store_id.id,
            }
            linked_stores.append(info)
        # linked_stores_info = [{'name': store['name'], 'id': store['id']} for store in linked_stores]
        # print(linked_stores_info)
        return JsonResponse({'success': True, 'form_data': form_data ,'linked_stores': linked_stores})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def save_tax_info(request, orgid):
    response_data = {}
    tempid = request.GET.get('tempid')
    org = Organization.objects.get(id=orgid)
    try:    
        temp = Taxes_Charges.objects.get(id=tempid)
    except:
        temp = None
    if request.method == 'POST':
        if temp:
            form = OrgTax(request.POST , instance = temp)
            if form.is_valid():
                tax_temp = form.save()
                
                response_data = {
                    'success' : True ,
                    'message' : '• Tax Template updated',
                    'status' : 'update' ,
                    'name' : tax_temp.tax_title,
                    'tempid' : tax_temp.id 
                }
            else:
                response_data = {
                    'error' : True ,
                    'message' : '• Couldn\'t save ,Error occured'
                    
                }
        else:
            form = OrgTax(request.POST)
            if form.is_valid():
                tax_temp = form.save(commit = False)
                tax_temp.org_id = org
                tax_temp.save()

                response_data = {
                    'success' : True ,
                    'message' : '• Tax Template saved',
                    'status' : 'new' ,
                    'name' : tax_temp.tax_title, 
                    'tempid' : tax_temp.id       
                }
            else:
                response_data = {
                    'error' : True ,
                    'message' : '• Couldn\'t save ,Error occured'
                    
                }
             
    return JsonResponse(response_data)

def delete_tax_info(request , temp_id):
    try:    
        tax_template = Taxes_Charges.objects.get(id=temp_id)
        tax_template.delete()
        response_data = {
            'success' : True ,
            'message' : '• Tax template deleted!' 
        }
    except:
        response_data = {
            'error' : True ,
            'message' : '• Error occured, couldn\'t delete!' 
        }
    
   
    return JsonResponse(response_data)


def add_store_tax(request , orgid , taxid , storeid):

    org = Organization.objects.get(id = orgid)
    tax_temp = Taxes_Charges.objects.get(id = taxid)
    store = Store.objects.get(id = storeid)
    
    Store_Tax.objects.create(org_id = org, tax_id = tax_temp, store_id = store)
    
    response_data = {
                    'success': True,
                    'message': f'• Tax applied for {store.name} store',
                    }
    return JsonResponse(response_data)

def delete_store_tax(request , orgid , taxid , storeid):

    org = Organization.objects.get(id = orgid)
    tax_temp = Taxes_Charges.objects.get(id = taxid)
    store = Store.objects.get(id = storeid)
    
    the_store_tax = Store_Tax.objects.get(org_id = org, tax_id = tax_temp, store_id = store)
    the_store_tax.delete()
    
    response_data = {
                    'success': True,
                    'message': f'• Tax removed from {store.name} store',
                    }
    return JsonResponse(response_data)


#----------------------------function of changing tax to pdf-------------------------------------
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def view_pdf(request, *args, **kwargs):
    # Assuming 'data' is defined somewhere in your code
    if request.method == 'POST':
        tax_data = json.loads(request.body.decode('utf-8'))
        
        tax_title = tax_data.get('tax_title')
        tax_include = tax_data.get('tax_include')
        default_value = tax_data.get('default')
        disable_value = tax_data.get('disable')
        min_amount = tax_data.get('min_amount')
        max_amount = tax_data.get('max_amount')
        tax_type = tax_data.get('tax_type')
        tax_amount = tax_data.get('tax_amount')
        rate = tax_data.get('rate')
        amount = tax_data.get('amount')

        # You can use these values to construct your context for rendering the PDF
        data = {
            'tax_title': tax_title,
            'tax_include': tax_include,
            'default': default_value,
            'disable': disable_value,
            'min_amount': min_amount,
            'max_amount': max_amount,
            'tax_type': tax_type,
            'tax_amount': tax_amount,
            'rate': rate,
            'amount': amount,
            # Add more fields as needed...
        }
        print(data)
        
        # unique_identifier = str(uuid.uuid4())
        pdf = render_to_pdf('galaxy/tax_pdf_template.html', data)
        # logging.debug(pdf)
        response = HttpResponse(pdf, content_type='application/pdf')   
        filename = f"{tax_title}_tax_info.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

# class ViewPDF(View):
#     def get(self, request, *args, **kwargs):
#         if request.method == 'GET':
#             data = {
#                 'tax_title': request.POST.get('salestaxDesc'),
#             }
            
#             pdf = render_to_pdf('galaxy/tax_pdf_template.html', data)
#             logging.debug(pdf)
#             response = HttpResponse(pdf, content_type='application/pdf')
#             response['Content-Disposition'] = 'inline; filename="tax_info.pdf"'
#             return response


def delete_department(request , orgid , depart_id):

    org = Organization.objects.get(id = orgid)
    department = Department.objects.get(id = depart_id , org_id = org)
    

    department.delete()
    
    response_data = {
                    'success': True,
                    'message': f'• Department {department.name} removed',
                    }
    return JsonResponse(response_data)

def add_department(request , orgid , code , name):

    org = Organization.objects.get(id = orgid)
    dep_name = f"{code}-{name}"
    department = Department.objects.create(org_id = org , name = dep_name)
    dep_id = department.id
    
    response_data = {
                    'success': True,
                    'message': f'• Department {dep_name} added',
                    'dep_id' : dep_id 
                    }
    return JsonResponse(response_data)