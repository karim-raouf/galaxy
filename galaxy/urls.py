from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

app_name = 'galaxy' 

urlpatterns = [
    path('', views.index , name = 'index'),
    
    path('pricing/', views.pricing , name = 'pricing'),
    path('about_us/', views.about_us , name = 'about_us'),
    path('contact_us/', views.contact_us , name = 'contact_us'),
    
    path('login/', views.login_page , name = 'login'),
    path('register/', views.signup_page , name = 'signup'),
    path('logout/', views.signout , name = 'logout'),
    
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='galaxy/password_reset.html') , name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='galaxy/password_reset_sent.html') , name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='galaxy/password_reset_form.html') , name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='galaxy/password_reset_done.html') , name = 'password_reset_complete'),

]