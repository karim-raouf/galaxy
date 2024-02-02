from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta , time
from .models import *
from galaxy.forms import *
from django.http import JsonResponse
import phonenumbers
import secrets
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_protect
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone , dateformat
import json
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.http import Http404
from galaxy.functions_utils import *


# Create your views here.

@login_required
def manage_user(request):
    if not get_referer(request):
        raise Http404
    
    user = request.user
    try:
        user_subs_basic = Subscription.objects.filter(UserID = user , Bundle_T = 'Basic')
    except:
        user_subs_basic = None
    try:
        users = System_User.objects.all()  #filter(SubscriptionID__UserID = user)
    except:
        users = None
    current_date = datetime.now().date()
    # the_user = None
    try:
        choosed_user = request.GET.get('id')
    except:
        choosed_user = None
    try:
        the_user = System_User.objects.get(id=choosed_user)
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
        session_model = Session.objects.using('app').filter(expire_date__gte=timezone.now())
        the_user_sessions = []
        the_user_sessions_info = []
        for session in session_model:
            # print(f"Session data from database: {session.session_data}")
            try:
                session_data = session.get_decoded()
                # print(f"Decoded session data: {session_data}")
            except Exception as decode_error:
                # print(f"Error decoding session data for session {session.session_key}: {decode_error}")
                continue
            if 'user_id' in session_data and session_data['user_id'] == the_user.id:
                ip_address = session_data.get('ip_address', 'N/A')
                location = session_data.get('location', 'N/A')
                start_time = session_data.get('start_time')
                session_store = SessionStore(session_key=session.session_key)
                the_user_sessions.append(session_store)

                # print('Session Data:', session_data)
                session_info = {
                    'session_id': session.session_key,
                    'ip_address': ip_address,
                    'location': location,
                    'start_time': start_time,
                }
                the_user_sessions_info.append(session_info)
                # print(the_user_sessions_info)
    except Exception as e:
        print(f'An error occurred: {e}')
        the_user_sessions = None
        the_user_sessions_info = None
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
               'the_user' : the_user ,
               'userform' : userform ,
               'pass_error' : pass_error ,
               'pass_error_user' : pass_error_user ,
               'user_module' : user_module ,
               'ip_addresses' : ip_addresses , 
               'the_user_sessions' : the_user_sessions,
               'time_restrictions' : time_restrictions,
               'the_user_sessions_info' : the_user_sessions_info
               }
    return render(request , 'management/manage_user.html' , context)



@csrf_protect
def add_allow_module(request):
 
    id = request.GET.get('id')
    user = System_User.objects.get(id = id)
    module_name = request.GET.get('module_name')
    module = Product.objects.get(Name = module_name , Type = 'Monthly')
    adding_module = AllowedModule.objects.create(UserId = user , module_code = module.Code , module_name = module_name)
 
    response_data = {
                    'success': True,
                    'message' : 'Module Added!'
                }
    
    return JsonResponse(response_data)


@csrf_protect
def delete_allow_module(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id = id)
    module_name = request.GET.get('module_name')
    module = Product.objects.get(Name = module_name , Type = 'Monthly')
    user_module = AllowedModule.objects.get(UserId = user , module_code = module.Code , module_name = module_name)
    user_module.delete()
    
    
    response_data = {
                    'success': True,
                    'message' : 'Module Removed!'
                }
  
    return JsonResponse(response_data)


@csrf_protect
def add_allow_ip(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id = id)
    ip_address = request.GET.get('ip_address')
    adding_address = AllowedIp.objects.create(UserId = user , ip_address = ip_address)
 
    response_data = {
                    'success': True,
                    'message' : 'IP Address Added!'
                }
  
    return JsonResponse(response_data)


@csrf_protect
def delete_allow_ip(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id = id)
    ip_address = request.GET.get('ip_address')
    user_ip = AllowedIp.objects.get(UserId = user , ip_address = ip_address)
    user_ip.delete()
    
    
    response_data = {
                    'success': True,
                    'message' : 'IP Address Removed!'
                }
  
    return JsonResponse(response_data)


@csrf_protect
def allow_all_ip(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id=id)
    user.ip_restricted = False
    user.save()
    
    response_data = {
                    'success': True,
                    'message' : 'All IPs Allowed!'
                }
  
    return JsonResponse(response_data)


@csrf_protect
def restrict_ip(request):
    
    user_id = request.GET.get('id')
    user = System_User.objects.get(id=user_id)
    user.ip_restricted = True
    user.save()
    access_users = AllowedIp.objects.filter(UserId=user)

    response_data = {
        'success': True,
        'message': 'Login IP Restricted!'
    }

    return JsonResponse(response_data)


@csrf_protect
def user_renew_on(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id=id)
    user.SubscriptionID.AutoRenew = True    
    user.SubscriptionID.save()
    
    response_data = {
                    'success': True,
                    'message' : 'Auto Renew ON!'
                }
  
    return JsonResponse(response_data)


@csrf_protect
def user_renew_off(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id=id)
    user.SubscriptionID.AutoRenew = False
    user.SubscriptionID.save()
    
    response_data = {
                    'success': True,
                    'message' : 'Auto Renew OFF!'
                }
  
    return JsonResponse(response_data)


@csrf_protect
def time_restrictions(request, user_id, day, start, end):
    
    user = System_User.objects.get(id=user_id)
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
        
    response_data = {
            'success': True,
            'message' : 'Access time saved!'
        }
    
    return JsonResponse(response_data)    
    

@csrf_protect
def remove_time_restrictions(request):
    
    id = request.GET.get('id')
    user = System_User.objects.get(id=id)
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

        the_user = System_User.objects.get(id=userid)
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
                elif password == password2 and len(password) >= 8 and re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?":{}|<>]', password) and re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
                    the_user = form.save(commit=False)
                    the_user.Psw_Flag = 0
                    the_user.save()
                    
                    session_model = Session.objects.using('app').filter(expire_date__gte=timezone.now())

                    for session in session_model:
                        session_data = session.get_decoded()
                        if 'user_id' in session_data and session_data['user_id'] == the_user.id:
                            session = AppSession.objects.get(session_key=session.session_key, expire_date__gte=timezone.now())
                            # session_store = SessionStore(session_key=session.session_key)
                            session.delete()


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
                        'pass_success': True,
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

                    session_model = Session.objects.using('app').filter(expire_date__gte=timezone.now())
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


@csrf_protect
def delete_user(request , id):
        if not get_referer(request):
            raise Http404
        # Get the code entered by the user      
        user_code = request.GET.get('code')
        # Get the code stored in the session
        stored_code = request.session.get('delete_code')
        if user_code == stored_code:
            user_id = id
            user = System_User.objects.get(id=user_id)
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
    
    
    
def session_del(request, session_id):
    try:
        # Retrieve the session instance
        session = AppSession.objects.get(session_key=session_id, expire_date__gte=timezone.now())
        # Delete the session
        session.delete()
        response_data = {
            'success': True,
            'message': '• Session deleted',
        }
    except Exception as e:
        print(f'An error occurred: {e}')
        response_data = {}

    return JsonResponse(response_data)


    
@login_required      
def manage_org(request):
    if not get_referer(request):
        raise Http404
    
    user = request.user
    org_subs = Subscription.objects.using('default').filter(UserID=user , ProductID__Code = 201)
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
               'org' : org ,
               'userform' : userform ,
               'pass_error' : pass_error ,
               'tax_temps' : tax_temps ,
               'tax_form' : tax_form , 
               'stores' : stores , 
               'applied_stores' : applied_stores,
               'departments' : departments,
               }
    
    
    return render(request , 'management/manage_org.html' , context)

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
            db_name = f'user_{request.user.id}'
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
            print('0')
            if not org_email:
                print('1')
                # messages.error(request,'• Organization Email Required')
                response_data = {
                    'error': True,
                    'message': '• Organization Email Required',
                }
            if not org_username:
                print('2')
                # messages.error(request,'• Organization Username Required')
                response_data = {
                    'error': True,
                    'message': '• Organization Username Required',
                }
            if any(org_username.lower() == name.OrganizationName.lower() for name in orgs):
                print('3')
                # messages.error(request,'• already using this organization name!')
                response_data = {
                    'error': True,
                    'message': '• already using this organization name!',
                }
            if not org_cost_method:
                print('4')
                # messages.error(request,'• Organization Cost Method Required')  
                response_data = {
                    'error': True,
                    'message': '• Organization Cost Method Required',
                }
            print(orgs)
            print(org)
            if org_email and org_username and org_cost_method and (org_username.lower() != organization.OrganizationName.lower() for organization in orgs):
                # messages.success(request,'Organization Saved Successfully!')
                print('5')
                org=form.save()
                response_data = {
                    'success': True,
                    'message': '• Organization Saved Successfully!',
                }

        else:
            print('6')
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
def render_to_pdf(template_src, context_dict=None):
    if context_dict is None:
        context_dict = {}

    template = get_template(template_src)
    html = template.render(context_dict)
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
    department = Department.objects.create(org_id = org , name = name , code = code)
    dep_id = department.id
    
    response_data = {
                    'success': True,
                    'message': f'• Department {name} added',
                    'dep_id' : dep_id 
                    }
    return JsonResponse(response_data)


def get_dep_categories(request, dep_id):
    try:
        selected_dep = Department.objects.get(id=dep_id)
        # tax_form = OrgTax(instance=selected_temp)
        related_categories = Category.objects.filter(department = selected_dep)
        dep_categories = []
    
        for category in related_categories:
            info = {
                'name' : category.name,
                'code' : category.code,
                'id' : category.id,
            }
            dep_categories.append(info)
        # linked_stores_info = [{'name': store['name'], 'id': store['id']} for store in linked_stores]
        print(dep_categories)
        return JsonResponse({'success': True, 'dep_categories': dep_categories})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    

def del_category(request , cat_id):

    category = Category.objects.get(id = cat_id)
    category.delete()
    
    response_data = {
    'success': True,
    'message': f'• Category {category.name} deleted',
    }
    return JsonResponse(response_data)

def add_category(request , depid , code , name):

    department = Department.objects.get(id = depid)
    category = Category.objects.create(department = department , name = name , code=code)
    cat_id = category.id
    
    response_data = {
                    'success': True,
                    'message': f'• category {name} added',
                    'cat_id' : cat_id 
                    }
    return JsonResponse(response_data)


def reportTemp(request):

    context = {}
    return render(request , "reports/ReportTemp.html" , context)