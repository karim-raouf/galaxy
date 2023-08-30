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
from django.db.models import Sum, Count


# Create your views here.

def index(request):
    switch_to_user_database('Users')
    user = request.user
    current_date = datetime.now().date()
    update_subscription_status(user, current_date)
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
            in_cart += 1
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
    context = {'user' : user , 'subed' : subed , 'org' : org , 'org_num' : org_num , 'cart' : cart , 'in_cart' : in_cart , 'total' : total}
    return render(request , 'galaxy/index.html' , context)
#update user--------------------------------------------------------------------------------------------------------------------------------------
def update_subscription_status(user, current_date):
    Subscription.objects.filter(UserID=user, EndDate=current_date).update(Status=False)
#--------------------------------------------------------------------------------------------------------------------------------------------------

def about_us(request):
    switch_to_user_database('Users')
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
            in_cart += 1
    #--------------------------------------------------------
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
    context = {'page_name' : 'About-us' , 'subed' : subed , 'org' : org , 'in_cart' : in_cart , 'cart' : cart , 'total' : total}
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
            in_cart += 1
    p_ids = []
    if cart:
        for item in cart:
            p_ids.append(item.ProductID.id)
        
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
    p_m = Product.objects.get(id=6)
    p_a = Product.objects.get(id=2)
    im_m = Product.objects.get(id=7)
    im_a = Product.objects.get(id=3)
    crm_m = Product.objects.get(id=8)
    crm_a = Product.objects.get(id=4)
    a_m = Product.objects.get(id=9)
    a_a = Product.objects.get(id=5)
    
    m_pos = Subscription.objects.filter( UserID=request.user , ProductID= p_m)
    a_pos = Subscription.objects.filter( UserID=request.user , ProductID= p_a)
    m_im = Subscription.objects.filter( UserID=request.user , ProductID= im_m)
    a_im = Subscription.objects.filter( UserID=request.user , ProductID= im_a)
    m_crm = Subscription.objects.filter( UserID=request.user , ProductID= crm_m)
    a_crm = Subscription.objects.filter( UserID=request.user , ProductID= crm_a)
    m_a = Subscription.objects.filter( UserID=request.user , ProductID= a_m)
    a_a = Subscription.objects.filter( UserID=request.user , ProductID= a_a)
    
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
               }
    return render(request , 'galaxy/pricing.html' , context)


def add_cart(request , id , type , b_type):
    user = request.user
    try:
        product = Product.objects.get(id=id)
        obj_cart = Cart.objects.get(UserID=user , ProductID=product , Type=type , Bundle_T=b_type)
        obj_cart.Qty += 1
        obj_cart.save()
    except:
        product = Product.objects.get(id=id)
        Cart.objects.create(UserID=user , ProductID=product , Type=type , Qty=1 , Bundle_T=b_type)
        return redirect('galaxy:pricing')
    return redirect('galaxy:pricing')

def delete_cart(request , id):
    obj = Cart.objects.get(UserID=request.user , ProductID=id)
    if obj.Qty > 1:
        obj.Qty -= 1
        obj.save()
    else:
        obj.delete()
    
    return redirect('galaxy:pricing')

def cart_total(request):
    total = 0
    item_in_cart = Cart.objects.filter(UserID=request.user)
    for item in item_in_cart:
        total += item.ProductID.Price * item.Qty
        
    # , id
@login_required
def payment(request):
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
                
                if item.Type == 'Monthly' and item.Bundle_T == 'Add-Ones':
                    for i in range(item.Qty):
                        Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_m , Type='Monthly' , Bundle_T='Add-Ones')
                
                if item.Type == 'Annually' and item.Bundle_T == 'Basic':
                    for i in range(item.Qty):
                        Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_m , Type='Annually' , Bundle_T='Basic')
                
                if item.Type == 'Annually' and item.Bundle_T == 'Add-Ones':
                    for i in range(item.Qty):
                        Subscription.objects.create( UserID = user, Status = True , ProductID= item.ProductID , AutoRenew = False , StartDate = current_date, EndDate = end_date_m , Type='Annually' , Bundle_T='Add-Ones')
            # try:
            #     create_user_database(str(user.username)+'_'+str(user.id))
            # except:
            #     pass
            cart_items.delete()
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
            in_cart += 1
    subed = None          
    user = request.user 
    org = None
    try:
        org = user.OrganizationID
        subed = user.subscription_set.filter(OrganizationID = org)
        
    except:
        subed  = False
    context = {'page_name' : 'Contact-us' , 'subed' : subed , 'org' : org , 'in_cart' : in_cart , 'cart' : cart , 'total' : total}
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
                return redirect('galaxy:index')
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


def my_products(request):
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
            in_cart += 1
    #----------------------------------------------------------------------------------
    
    sub_basic = Subscription.objects.filter(UserID=request.user ,  Bundle_T='Basic')
    sub_add = Subscription.objects.filter(UserID=request.user, Bundle_T='Add-Ones').values('ProductID__Code', 'ProductID__Name').annotate(total_qty=Count('ProductID__Code'))
    
    context = {'sub_basic' : sub_basic,'sub_add' : sub_add ,'in_cart' : in_cart , 'cart' : cart , 'total' : total}
    return render(request , 'galaxy/my_products.html' , context)

        

