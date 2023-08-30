from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

app_name = 'galaxy' 

urlpatterns = [
    path('', views.index , name = 'index'),
    
    path('pricing/', views.pricing , name = 'pricing'),
    path('about_us/', views.about_us , name = 'about_us'),
    path('contact_us/', views.contact_us , name = 'contact_us'),
    path('my_products/', views.my_products , name = 'my_products'),
    
    
    path('login/', views.login_page , name = 'login'),
    path('register/', views.signup_page , name = 'signup'),
    path('logout/', views.signout , name = 'logout'),
    path('profile/', views.profile , name = 'profile'),
    path('profile_edit/', views.profile_edit , name = 'profile_edit'),
    #  
    path('payment/', views.payment , name = 'payment'),
    path('organization/', views.choose_org , name = 'org_choose'),
    path('success/', views.success , name = 'success_m'),
    path('upgrade_success/', views.update_success , name = 'u_success_m'),
    path('activate/<uidb64>/<token>', views.activate , name = 'activate'),
    path('activate_link/', views.activation_msg , name = 'activate_msg'),
    path('activate_done/', views.activation_done , name = 'activate_done'),
    path('add_cart/<int:id>/<str:type>/<str:b_type>', views.add_cart , name = 'add_cart'),
    path('delete_cart/<int:id>', views.delete_cart , name = 'delete_cart'),
    
    
    
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='galaxy/password_reset.html') , name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='galaxy/password_reset_sent.html') , name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='galaxy/password_reset_form.html') , name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='galaxy/password_reset_done.html') , name = 'password_reset_complete'),

]