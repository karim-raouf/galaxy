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
    path('my_products/organizations', views.manage_org , name = 'manage_org'),
    path('my_products/organizations/delete_org/<int:id>', views.delete_org , name = 'delete_org'),
    path('my_products/users', views.manage_user , name = 'manage_user'),
    path('my_products/users/delete_user/<int:id>', views.delete_user , name = 'delete_user'),


    

    
   
    
    path('login/', views.login_page , name = 'login'),
    path('register/', views.signup_page , name = 'signup'),
    path('logout/', views.signout , name = 'logout'),
    path('pass_reset', views.pass_reset , name = 'pass_reset'),
    # path('profile/', views.profile , name = 'profile'),  
    path('payment/', views.payment , name = 'payment'),
    path('promo_code/<str:code>/<int:total>', views.applying_promocode , name='apply_promo'),
    path('add_allow_module/', views.add_allow_module , name='add_allow_module'),
    path('delete_allow_module/', views.delete_allow_module , name='delete_allow_module'),
    path('add_allow_ip/', views.add_allow_ip , name='add_allow_ip'),
    path('delete_allow_ip/', views.delete_allow_ip , name='delete_allow_ip'),
    path('allow_all_ip/', views.allow_all_ip , name='allow_all_ip'),
    path('restrict_ip/', views.restrict_ip , name='restrict_ip'),
    
    
    path('user_autorenow_on/', views.user_renew_on , name='user_renew_on'),
    path('user_autorenow_off/', views.user_renew_off , name='user_renew_off'),
    path('org_autorenow_on/', views.org_renew_on , name='org_renew_on'),
    path('org_autorenow_off/', views.org_renew_off , name='org_renew_off'),
    path('time_restrictions/',views.time_restrictions, name='time_restrictions'),
    path('remove_time_restrictions/',views.remove_time_restrictions, name='remove_time_restrictions'),






    

    path('organization/', views.choose_org , name = 'org_choose'),
    path('success/', views.success , name = 'success_m'),
    path('upgrade_success/', views.update_success , name = 'u_success_m'),
    path('activate/<uidb64>/<token>', views.activate , name = 'activate'),
    path('activate_link/', views.activation_msg , name = 'activate_msg'),
    path('activate_done/', views.activation_done , name = 'activate_done'),
    path('add_cart/<int:id>/<str:type>/<str:b_type>', views.add_cart , name = 'add_cart'),
    path('delete_cart/<int:id>', views.delete_cart , name = 'delete_cart'),
    path('change_pass/', views.pass_change , name = 'change_pass'),

    
    
    
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='galaxy/password_reset.html') , name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='galaxy/password_reset_sent.html') , name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='galaxy/password_reset_form.html') , name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='galaxy/password_reset_done.html') , name = 'password_reset_complete'),

]