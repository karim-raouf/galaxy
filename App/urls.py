from django.urls import path 
from . import views

app_name = 'App'    

urlpatterns = [
    path('', views.apphome , name = 'apphome'),
    path('default_db', views.default_db , name = 'default_db'),  
    
]