from django.urls import path 
from . import views


urlpatterns = [
    
    #---------------user management---------------
    path('my_products/users', views.manage_user , name = 'manage_user'),
    path('add_allow_module/', views.add_allow_module , name='add_allow_module'),
    path('delete_allow_module/', views.delete_allow_module , name='delete_allow_module'),
    path('add_allow_ip/', views.add_allow_ip , name='add_allow_ip'),
    path('delete_allow_ip/', views.delete_allow_ip , name='delete_allow_ip'),
    path('allow_all_ip/', views.allow_all_ip , name='allow_all_ip'),
    path('restrict_ip/', views.restrict_ip , name='restrict_ip'),
    path('user_autorenow_on/', views.user_renew_on , name='user_renew_on'),
    path('user_autorenow_off/', views.user_renew_off , name='user_renew_off'),
    path('time_restrictions/<int:user_id>/<str:day>/<str:start>/<str:end>',views.time_restrictions, name='time_restrictions'),
    path('remove_time_restrictions/',views.remove_time_restrictions, name='remove_time_restrictions'),
    path('my_products/users/save_system_user/<int:userid>', views.save_system_user , name = 'save_system_user'),
    path('my_products/users/delete_user/<int:id>', views.delete_user , name = 'delete_user'),
    path('session_delete/<str:session_id>', views.session_del , name='session_delete'),
    
    #-------------organization management-----------
    
    path('my_products/organizations', views.manage_org , name = 'manage_org'),
    path('my_products/organizations/delete_org/<int:id>', views.delete_org , name = 'delete_org'),
    path('my_products/organizations/<int:orgid>', views.save_org , name = 'save_org'),
    path('my_products/organizations/tax_info/<int:orgid>', views.save_tax_info , name = 'save_tax_info'),
    path('my_products/organizations/tax_info/delete/<int:temp_id>', views.delete_tax_info , name = 'delete_tax_info'),
    path('my_products/organizations/tax_info/add_store_tax/<int:orgid>/<int:taxid>/<int:storeid>', views.add_store_tax , name = 'add_store_tax'),
    path('my_products/organizations/tax_info/delete_store_tax/<int:orgid>/<int:taxid>/<int:storeid>', views.delete_store_tax , name = 'delete_store_tax'),
    path('org_tax_info/<int:temp_id>', views.get_tax_data , name='org_tax_info'),
    path('my_products/organizations/departments/delete_dep/<int:orgid>/<int:depart_id>', views.delete_department , name = 'delete_departement'),
    path('my_products/organizations/departments/add_dep/<int:orgid>/<int:code>/<str:name>', views.add_department , name = 'add_departement'),
    path('org_dep_categories/<int:dep_id>', views.get_dep_categories , name='org_dep_categories'),
    path('my_products/organizations/departments/categories/delete/<int:cat_id>', views.del_category , name='delete_category'),
    path('my_products/organizations/departments/categories/add_cat/<int:depid>/<int:code>/<str:name>', views.add_category , name = 'add_category'),
    path('org_autorenow_on/', views.org_renew_on , name='org_renew_on'),
    path('org_autorenow_off/', views.org_renew_off , name='org_renew_off'),
    path('pdf_view/', views.view_pdf, name="pdf_view"),
    path('Reports/ReportTemp', views.reportTemp, name="reportTemp"),

]