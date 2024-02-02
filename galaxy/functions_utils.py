from .models import *
from datetime import datetime


def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer


def update_subscription_status(user):
    current_date = datetime.now().date()
    Subscription.objects.filter(UserID=user, EndDate=current_date).update(Status=False)
    
    
# def get_user_location(request):
#     # Get the user's IP address
#     user_ip = get_client_ip(request)
#     # user_ip = '197.53.227.100'
#     # Make a request to ipinfo.io to get location information
#     ipinfo_token = 'e2e096db330bce'  # Replace with your ipinfo.io token
#     api_url = f'https://ipinfo.io/{user_ip}?token={ipinfo_token}'

#     try:
#         response = requests.get(api_url)
#         data = response.json()

#         # Extract latitude and longitude
#         location = data.get('loc', 'N/A')

#         # Return the formatted location information
#         return location
#     except Exception as e:
#         # Handle any errors (e.g., network issues, API rate limits)
#         print(f"Error getting location: {e}")
#         return 'N/A'


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


# def check_time_restrictions(user):
#     try:
#         current_time = datetime.now().time()
#         current_day = datetime.now().strftime('%A')

#         time_restrictions = user.timerestriction_set.filter(day_of_week=current_day)
#         if time_restrictions.exists():
#             for restriction in time_restrictions:
#                 try:
#                     start_time = restriction.start_time
#                     end_time = restriction.end_time
#                     if start_time <= current_time < end_time:
#                         return True
#                 except Exception as e:
#                     print(f"An error occurred while comparing time values: {str(e)}")
#                     return False
#         else:
#             # No time restrictions for the current day
#             return True
#       # return False
#     except Exception as e:
#         print(f"An error occurred while checking time restrictions: {str(e)}")
#         return False