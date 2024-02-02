from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission,  AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

SUBTYPE = (
    ('Monthly' , 'Monthly'),
    ('Annually' , 'Annually'),
)
BUNTYPE = (
    ('Basic' , 'Basic'),
    ('Add-Ons' , 'Add-Ons'),
)
COSTMETH = (
    ( 1 , 'Weighted average'),
    ( 2 , 'In first - Out first'),
)
GENDER = (
    ( 1 , 'Male'),
    ( 2 , 'Female'),
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


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)
        
class User(AbstractUser):
    email = models.EmailField(unique = True , null = True , blank=True) 
    password = models.CharField(max_length=128, null=True, blank=True)
    Psw_Flag = models.IntegerField(null = True , blank = True)
    username = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(upload_to='user_images/' , null = True , blank = True)
    # user_Type = models.ForeignKey('UsersType' , on_delete=models.SET_NULL ,blank=True, null=True)
    SubscriptionID = models.ForeignKey('Subscription' , on_delete=models.CASCADE , null=True , blank=True)
    Language = models.ForeignKey('Language' , on_delete=models.SET_NULL , null=True , blank=True)
    Birth_Date = models.DateField(verbose_name="Birth Date" , null=True , blank=True)
    Gender = models.IntegerField(choices=GENDER , null=True, blank=True)
    Telephone = models.CharField(max_length=100 , unique=True , null=True , blank=True)
    ip_restricted = models.BooleanField(default=False)
    system_user_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return '(' + str(self.email)+'-'+str(self.id)+')'
    
    

# class Organization(models.Model):
#     UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
#     SubscriptionID = models.ForeignKey('Subscription' , on_delete=models.CASCADE , null=True)#, limit_choices_to={'ProductID': 17}
#     Com_Regm = models.FileField("Upload Commercial registration :",upload_to='file_uploads/' , null=True , blank=True)
#     Tax_Reg = models.FileField("Upload the Tax registration :",upload_to='file_uploads/' , null=True, blank=True)
#     Logo = models.ImageField("Upload the Logo :",upload_to='org_logos/', null = True, blank=True)
#     Report_B =models.ImageField("Upload Reports & Letters Bottom :",upload_to='reports_b/' ,null = True, blank=True)
#     Report_H =models.ImageField("Upload Reports & Letters Header :",upload_to='reports_h/' ,null = True, blank=True)
#     OrganizationName = models.CharField('Organization Name :',max_length = 50 , null = True , blank=True)
#     OrganizationEmail = models.EmailField(unique = True , null = True, blank=True)
#     Address = models.CharField("Address :",max_length=100 , null=True, blank=True)
#     Country = models.ForeignKey('Country',verbose_name="Country :" , on_delete=models.SET_NULL , null=True, blank=True)
#     Currency = models.ForeignKey('Currency' ,verbose_name="Currency :" ,on_delete=models.SET_NULL , null=True, blank=True)
#     # Tax = models.ForeignKey('Tax' ,verbose_name="Tax :" ,on_delete=models.SET_NULL , null=True, blank=True)
#     Cost_Method = models.IntegerField("Calculate item cost as :" ,choices=COSTMETH , null=True, blank=True)
#     Create_Receive = models.BooleanField("Automaticlly create inter-store receive inventory orders :" , default=False)
#     Create_Issue = models.BooleanField("Automaticlly create inter-store issue inventory orders :", default=False)
#     Terms = models.TextField("Default Terms and Conditions :",null=True, blank=True) 
#     WebsiteLink = models.URLField(max_length=200 , null = True, blank=True)
#     WhatsappLink = models.URLField(max_length=200 , null = True, blank=True)
#     FacebookLink = models.URLField(max_length=200 , null = True, blank=True)
#     InstagramLink = models.URLField(max_length=200 , null = True, blank=True)
#     CreatedDate = models.DateField(verbose_name="Created Date" , null=True)
    
    
#     def __str__(self):
#         return str(self.UserID)+' ('+str(self.OrganizationName) + ')'
    

class Subscription(models.Model):
    
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    Status = models.BooleanField(null=True)
    StartDate = models.DateField(verbose_name="Start Date",null=True)
    EndDate = models.DateField(verbose_name="End Date",null=True)
    ProductID = models.ForeignKey('Product' , on_delete=models.SET_NULL , null=True)
    AutoRenew = models.BooleanField()
    Type = models.CharField(max_length=20 , choices=SUBTYPE , null=True)
    Bundle_T = models.CharField(max_length=20 , choices=BUNTYPE , null=True)
    
    def __str__(self):
        return str(self.ProductID)+'-'+str(self.UserID)+'_'+str(self.id)
    
    

class Account(models.Model):   
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    Balanace = models.DecimalField(max_digits=10, decimal_places=2)
    CreditLimit = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.UserID.email
    
    
class Product(models.Model):
    Name = models.CharField(max_length=50)
    Type = models.CharField(max_length=20 , choices=SUBTYPE , null=True)
    Price = models.IntegerField()
    Bundle_T = models.CharField(max_length=20 , choices=BUNTYPE , null=True)
    Code = models.IntegerField(null=True)
    
    def __str__(self):
        return (self.Name)+'-'+(self.Type)
    

class Cart(models.Model):
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    Qty = models.IntegerField()
    Type = models.CharField(max_length=20 , choices=SUBTYPE , null=True)
    ProductID = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True)
    Bundle_T = models.CharField(max_length=20 , choices=BUNTYPE , null=True)
    
    def __str__(self):
        return str(self.UserID)+'-'+str(self.ProductID)
    
    
# class Country(models.Model):
#     name = models.CharField(max_length=50 , null=True)
    
#     def __str__(self):
#         return self.name
    
    
    
# class Currency(models.Model):
#     name = models.CharField(max_length=50 , null=True)

#     def __str__(self):
#         return self.name
    
    
# class Taxes_Charges(models.Model):  
#     org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True , blank=True)
#     tax_title = models.CharField(max_length=50 , null=True , blank=True)
#     tax_include = models.BooleanField()
#     default = models.BooleanField()
#     disable = models.BooleanField()
#     min_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     max_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     tax_type = models.IntegerField(choices=TAXTYPE, null=True)
#     tax_amount  = models.IntegerField(choices=TAXAMOUNT, null=True)
#     rate =  models.DecimalField(max_digits=5, decimal_places=2)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    
#     def __str__(self):
#         return str(self.org_id) + ' (' + self.tax_title + ')'
        
    
# class Store_Tax(models.Model):
#     org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True , blank=True)
#     tax_id = models.ForeignKey('Taxes_Charges' , on_delete=models.CASCADE , null=True , blank=True)
#     store_id = models.ForeignKey('Store' , on_delete=models.CASCADE , null=True , blank=True)
    
#     def __str__(self):
#         return str(str(self.org_id.UserID) + ' (' +self.store_id.name + ' (' + self.tax_id.tax_title + '))')
    

    
    
# class Store(models.Model):
#     org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True , blank=True)
#     name = models.CharField(max_length=50 , null=True )
    
#     def __str__(self):
#         return str(self.name)   

# class UsersType(models.Model):
#     UserTypeCode = models.IntegerField(null = True)
#     UserTypeName = models.CharField(max_length=50 , null = True)
    
#     def __str__(self):
#         return self.UserTypeName
    
    
class Language(models.Model):
    language = models.CharField(max_length=50 , unique=True)
    
    def __str__(self):
        return self.language
    
class PromoCode(models.Model):
    code = models.CharField(max_length = 20 , null=True , blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    usercode = models.ForeignKey(User, on_delete=models.CASCADE , null=True , blank=True)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.discount)+'-'+str(self.usercode)
    
    
# class AllowedModule(models.Model):
#     UserId = models.ForeignKey(User , on_delete=models.CASCADE)
#     module_code = models.IntegerField(null=True)
#     module_name = models.CharField(max_length=50 , null=True)
    
#     def __str__(self):
#         return str(self.UserId)+"-"+"("+str(self.module_name)+'-'+str(self.module_code)+")"
    

# class AllowedIp(models.Model):
#     UserId = models.ForeignKey(User , on_delete=models.CASCADE)
#     ip_address = models.GenericIPAddressField(null = True)
    
#     def __str__(self):
#         return str(self.UserId)+"-"+"("+str(self.ip_address)+")"
    
    
# class TimeRestriction(models.Model):
#     UserID = models.ForeignKey(User, on_delete=models.CASCADE)
#     day_of_week = models.CharField(max_length=10 , null=True , blank=True)
#     start_time = TimeFormatField()
#     end_time = TimeFormatField()
    
#     def __str__(self):
#         return str(self.UserID)+'('+str(self.day_of_week)+')'
    
# class Department(models.Model):
#     name =  models.CharField(max_length=30 , null=True)
#     code = models.CharField(max_length=17 , null=True)
#     org_id = models.ForeignKey('Organization' , on_delete=models.CASCADE , null=True)
    
#     def __str__(self):
#         return str(self.org_id) + '(' + self.name + ')'
    
    
# class Category(models.Model):
#     name =  models.CharField(max_length=30 , null=True)
#     code = models.CharField(max_length=17 , null=True)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.department) +'(' + self.name + ')'
    