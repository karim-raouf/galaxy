# middleware.py
from django.contrib.auth import logout
from datetime import datetime, timedelta
from .models import *
from django.contrib import messages
from project.settings import switch_database
from .functions_utils import *


class ChangeDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        try:
            if user.is_anonymous:   
                switch_database(f"user_133") 
            else:
                have_db = Subscription.objects.filter(UserID = user , ProductID__Code = 201)
                if have_db:
                    print(f"user_{user.id}")
                    switch_database(f"user_{user.id}")
                else:
                    switch_database(f"user_133") 
        except Exception as e:         
            print(f'An error occurred: {e}')
            
        response = self.get_response(request)
        return response
    
    
class UpdateSubStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_anonymous:
            update_subscription_status(user)
        response = self.get_response(request)
        return response
    

# class TimeRestrictionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user
#         try:
#             time_restrictions = TimeRestriction.objects.filter(UserID=user)
#         except:
#             time_restrictions = None
#         if user.is_authenticated and time_restrictions:
#             current_time = datetime.now().time()
#             current_day = datetime.now().strftime('%A').lower()

#             for restriction in time_restrictions:
#                 # Check if the current day matches the time restriction day
#                 if current_day == restriction.day_of_week.lower() and current_time > restriction.end_time:
#                     logout(request)
#         response = self.get_response(request)
#         return response


# class IpRestrictionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user
#         ip_address_found = False
#         try:
#             ip_restrictions = AllowedIp.objects.filter(UserId=user)
#         except:
#             pass
#             ip_restrictions = None
#         if user is not None and user.is_authenticated and user.ip_restricted:
#             if ip_restrictions:
#                 for restriction in ip_restrictions:
#                     if get_client_ip(request) == restriction.ip_address:
#                         ip_address_found = True
#                         break

#                 if not ip_address_found:
#                     logout(request)
#                     messages.error(request, "Logged out. your IP is not allowed to this user")


#             else:
#                 logout(request)
#                 messages.error(request, "Logged out. your IP is not allowed to this user")

#         response = self.get_response(request)
#         return response
    
# class PswFlagMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user
#         login_page_url = '/login/'
#         pass_reset_url = '/pass_reset/'  # Replace with your desired URL or path
#         if user.is_authenticated and user.Psw_Flag == 0 and request.path != pass_reset_url:
#             if request.path != login_page_url: 
#                 logout(request)
#         response = self.get_response(request)
#         return response
    
    