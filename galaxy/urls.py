from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views
from urllib.parse import quote


# app_name = 'galaxy' 

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
    path('my_products/users/save_system_user/<int:userid>', views.save_system_user , name = 'save_system_user'),
    path('my_products/organizations/<int:orgid>', views.save_org , name = 'save_org'),
    path('my_products/organizations/tax_info/<int:orgid>', views.save_tax_info , name = 'save_tax_info'),
    path('my_products/organizations/tax_info/delete/<int:temp_id>', views.delete_tax_info , name = 'delete_tax_info'),
    path('my_products/organizations/tax_info/add_store_tax/<int:orgid>/<int:taxid>/<int:storeid>', views.add_store_tax , name = 'add_store_tax'),
    path('my_products/organizations/tax_info/delete_store_tax/<int:orgid>/<int:taxid>/<int:storeid>', views.delete_store_tax , name = 'delete_store_tax'),
    path('org_tax_info/<int:temp_id>', views.get_tax_data , name='org_tax_info'),
    path('my_products/organizations/departments/delete_dep/<int:orgid>/<int:depart_id>', views.delete_department , name = 'delete_departement'),
    path('my_products/organizations/departments/add_dep/<int:orgid>/<int:code>/<str:name>', views.add_department , name = 'add_departement'),

    
    
    
    path('pdf_view/', views.view_pdf, name="pdf_view"),



   
    
    path('login/', views.login_page , name = 'login'),
    path('register/', views.signup_page , name = 'signup'),
    path('logout/', views.signout , name = 'logout'),
    path('pass_reset/', views.pass_reset , name = 'pass_reset'),
    # path('profile/', views.profile , name = 'profile'),  
    path('payment/', views.payment , name = 'payment'),
    path('promo_code/<str:code>/<int:total>', views.applying_promocode , name='apply_promo'),
    path('add_allow_module/', views.add_allow_module , name='add_allow_module'),
    path('delete_allow_module/', views.delete_allow_module , name='delete_allow_module'),
    path('add_allow_ip/', views.add_allow_ip , name='add_allow_ip'),
    path('delete_allow_ip/', views.delete_allow_ip , name='delete_allow_ip'),
    path('allow_all_ip/', views.allow_all_ip , name='allow_all_ip'),
    path('restrict_ip/', views.restrict_ip , name='restrict_ip'),
    path('session_delete/<str:session_id>', views.session_del , name='session_delete'),
    
 

    
    
    
    
    path('user_autorenow_on/', views.user_renew_on , name='user_renew_on'),
    path('user_autorenow_off/', views.user_renew_off , name='user_renew_off'),
    path('org_autorenow_on/', views.org_renew_on , name='org_renew_on'),
    path('org_autorenow_off/', views.org_renew_off , name='org_renew_off'),
    path('time_restrictions/<int:user_id>/<str:day>/<str:start>/<str:end>',views.time_restrictions, name='time_restrictions'),
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
    
    
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='galaxy/password_reset.html') , name = "password_reset" ),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='galaxy/password_reset_sent.html') , name = "password_reset_done" ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='galaxy/password_reset_form.html') , name = "password_reset_confirm" ),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='galaxy/password_reset_done.html') , name = "password_reset_complete" ),

]