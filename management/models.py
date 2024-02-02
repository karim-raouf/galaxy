from django.db import models
from galaxy.models import *
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from galaxy.timeformatfield import TimeFormatField

# Create your models here.

# Group.add_to_class('users', models.ManyToManyField('User', related_name='management_user_groups', blank=True))
# Permission.add_to_class('users', models.ManyToManyField('User', related_name='management_user_permissions', blank=True))

COSTMETH = (
    ( 1 , 'Weighted average'),
    ( 2 , 'In first - Out first'),
)

TAXTYPE=(
(1 , 'On the net total of the item'),
(2 , 'On Previous Row Amount'),
(3 , 'On Previous Row Total'),
)

TAXAMOUNT=(
    (4 , 'Fixed Amount'),
    (5 , 'Rate'),
    (6 , 'Fixed Amount + Rate'),
    (7 , 'Enter the rate manualy'),
)  


class CustomGroup(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='management_user_groups', blank=True)
    # Other fields

    class Meta:
        db_table = 'galaxy_custom_group'
        managed = False
        
        
class CustomPermission(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='management_user_permissions', blank=True)
    # Other fields

    class Meta:
        db_table = 'galaxy_custom_permission'
        managed = False


class AppSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        db_table = 'django_session'
        managed = False


class System_User(AbstractUser):
    email = models.EmailField(unique = True , null = True , blank=True) 
    password = models.CharField(max_length=128, null=True, blank=True)
    Psw_Flag = models.IntegerField(null = True , blank = True)
    username = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(upload_to='user_images/' , null = True , blank = True)
    user_Type = models.ForeignKey('UsersType' ,related_name='app_user_types', on_delete=models.SET_NULL ,blank=True, null=True)
    SubscriptionID = models.ForeignKey(Subscription ,related_name='app_user_subscription', on_delete=models.CASCADE , null=True , blank=True)
    Language = models.ForeignKey(Language ,related_name='app_user_language', on_delete=models.SET_NULL , null=True , blank=True)
    Birth_Date = models.DateField(verbose_name="Birth Date" , null=True , blank=True)
    Gender = models.IntegerField(choices=GENDER , null=True, blank=True)
    Telephone = models.CharField(max_length=100 , unique=True , null=True , blank=True)
    ip_restricted = models.BooleanField(default=False)
    system_user_active = models.BooleanField(default=True)
    
    groups = models.ManyToManyField('management.CustomGroup', related_name='galaxy_user_group', blank=True)
    user_permissions = models.ManyToManyField('management.CustomPermission', related_name='galaxy_user_permission', blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return '(' + str(self.email)+'-'+str(self.id)+')'
    
    class Meta:
        db_table = 'galaxy_user'
        managed = False
        
        
class Organization(models.Model):
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    SubscriptionID = models.ForeignKey(Subscription , on_delete=models.SET_NULL , null=True)#, limit_choices_to={'ProductID': 17}
    Com_Regm = models.FileField("Upload Commercial registration :",upload_to='file_uploads/' , null=True , blank=True)
    Tax_Reg = models.FileField("Upload the Tax registration :",upload_to='file_uploads/' , null=True, blank=True)
    Logo = models.ImageField("Upload the Logo :",upload_to='org_logos/', null = True, blank=True)
    Report_B =models.ImageField("Upload Reports & Letters Bottom :",upload_to='reports_b/' ,null = True, blank=True)
    Report_H =models.ImageField("Upload Reports & Letters Header :",upload_to='reports_h/' ,null = True, blank=True)
    OrganizationName = models.CharField('Organization Name :',max_length = 50 , null = True)
    OrganizationEmail = models.EmailField(unique = True , null = True, blank=True)
    Address = models.CharField("Address :",max_length=100 , null=True, blank=True)
    Country = models.ForeignKey('Country',verbose_name="Country :" , on_delete=models.SET_NULL , null=True, blank=True)
    Currency = models.ForeignKey('Currency' ,verbose_name="Currency :" ,on_delete=models.SET_NULL , null=True, blank=True)
    Cost_Method = models.IntegerField("Calculate item cost as :" ,choices=COSTMETH , null=True, blank=True)
    Create_Receive = models.BooleanField(default=False)
    Create_Issue = models.BooleanField(default=False)
    Terms = models.TextField("Default Terms and Conditions :",null=True, blank=True) 
    WebsiteLink = models.URLField(max_length=200 , null = True, blank=True)
    WhatsappLink = models.URLField(max_length=200 , null = True, blank=True)
    FacebookLink = models.URLField(max_length=200 , null = True, blank=True)
    InstagramLink = models.URLField(max_length=200 , null = True, blank=True)
    CreatedDate = models.DateField(verbose_name="Created Date" , null=True)
    
    
    def __str__(self):
        return str(self.OrganizationName) 
    
    class Meta:
        db_table = 'galaxy_organization'
        managed = False
        
        
class Country(models.Model):
    name = models.CharField(max_length=50 , null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'galaxy_country'
        managed = False



class Currency(models.Model):
    name = models.CharField(max_length=50 , null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'galaxy_currency'
        managed = False
        


class Taxes_Charges(models.Model):  
    org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True , blank=True)
    tax_title = models.CharField(max_length=50 , null=True , blank=True)
    tax_include = models.BooleanField()
    default = models.BooleanField()
    disable = models.BooleanField()
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_type = models.IntegerField(choices=TAXTYPE, null=True)
    tax_amount  = models.IntegerField(choices=TAXAMOUNT, null=True)
    rate =  models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    
    def __str__(self):
        return str(self.org_id) + ' (' + self.tax_title + ')'
    
    class Meta:
        db_table = 'galaxy_taxes_charges'
        managed = False
        

class Store_Tax(models.Model):
    org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True , blank=True)
    tax_id = models.ForeignKey('Taxes_Charges' , on_delete=models.CASCADE , null=True , blank=True)
    store_id = models.ForeignKey('Store' , on_delete=models.CASCADE , null=True , blank=True)
    
    def __str__(self):
        return str(str(self.org_id.UserID) + ' (' +self.store_id.name + ' (' + self.tax_id.tax_title + '))')
    
    class Meta:
        db_table = 'galaxy_store_tax'
        managed = False
    
    
    
class Store(models.Model):
    org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=50 , null=True )
    
    def __str__(self):
        return str(self.name)   
    
    class Meta:
        db_table = 'galaxy_store'
        managed = False
        


class UsersType(models.Model):
    UserTypeCode = models.IntegerField(null = True)
    UserTypeName = models.CharField(max_length=50 , null = True)
    
    def __str__(self):
        return self.UserTypeName
    
    class Meta:
        db_table = 'galaxy_userstype'
        managed = False
    
    
    
# class Language(models.Model):
#     language = models.CharField(max_length=50 , unique=True)
    
#     def __str__(self):
#         return self.language
    
#     class Meta:
#         db_table = 'galaxy_language'
#         managed = False
        


class AllowedModule(models.Model):
    UserId = models.ForeignKey(System_User , on_delete=models.CASCADE)
    module_code = models.IntegerField(null=True)
    module_name = models.CharField(max_length=50 , null=True)
    
    def __str__(self):
        return str(self.UserId)+"-"+"("+str(self.module_name)+'-'+str(self.module_code)+")"
    
    class Meta:
        db_table = 'galaxy_allowedmodule'
        managed = False
    

class AllowedIp(models.Model):
    UserId = models.ForeignKey(System_User , on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null = True)
    
    def __str__(self):
        return str(self.UserId)+"-"+"("+str(self.ip_address)+")"
    
    class Meta:
        db_table = 'galaxy_allowedip'
        managed = False
    
    
class TimeRestriction(models.Model):
    UserID = models.ForeignKey(System_User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10 , null=True , blank=True)
    start_time = TimeFormatField()
    end_time = TimeFormatField()
    
    def __str__(self):
        return str(self.UserID)+'('+str(self.day_of_week)+')'
    
    class Meta:
        db_table = 'galaxy_timerestriction'
        managed = False
        
        
    
class Department(models.Model):
    name =  models.CharField(max_length=30 , null=True)
    code = models.CharField(max_length=17 , null=True)
    org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True)
    
    def __str__(self):
        return str(self.org_id) + '(' + self.name + ')'
    
    class Meta:
        db_table = 'galaxy_department'
        managed = False
    
    
    
class Category(models.Model):
    name =  models.CharField(max_length=30 , null=True)
    code = models.CharField(max_length=17 , null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.department) +'(' + self.name + ')'
    
    class Meta:
        db_table = 'galaxy_category'
        managed = False