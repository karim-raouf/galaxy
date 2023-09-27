from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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



class User(AbstractUser):
    email = models.EmailField(unique = True , null = True , blank=True) 
    password = models.CharField(max_length=128, null=True, blank=True)
    Psw_Flag = models.IntegerField(null = True , blank = True)
    username = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.ImageField(upload_to='user_images/' , null = True , blank = True)
    user_Type = models.ForeignKey('UsersType' , on_delete=models.SET_NULL , null=True)
    SubscriptionID = models.ForeignKey('Subscription' , on_delete=models.SET_NULL , null=True , blank=True)
    Language = models.ForeignKey('Language' , on_delete=models.SET_NULL , null=True , blank=True)
    Birth_Date = models.DateField(verbose_name="Birth Date" , null=True , blank=True)
    Gender = models.IntegerField(choices=GENDER , null=True, blank=True)
    Telephone = models.CharField(max_length=100 , unique=True , null=True , blank=True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return str(self.email)+'-'+str(self.id)
    
    

class Organization(models.Model):
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    SubscriptionID = models.ForeignKey('Subscription' , on_delete=models.SET_NULL , null=True)#, limit_choices_to={'ProductID': 17}
    Com_Regm = models.FileField("Upload Commercial registration :",upload_to='file_uploads/' , null=True , blank=True)
    Tax_Reg = models.FileField("Upload the Tax registration :",upload_to='file_uploads/' , null=True, blank=True)
    Logo = models.ImageField("Upload the Logo :",upload_to='org_logos/', null = True, blank=True)
    Report_B =models.ImageField("Upload Reports & Letters Bottom :",upload_to='reports_b/' ,null = True, blank=True)
    Report_H =models.ImageField("Upload Reports & Letters Header :",upload_to='reports_h/' ,null = True, blank=True)
    OrganizationName = models.CharField('Organization Name :',max_length = 50 , null = True , blank=True)
    OrganizationEmail = models.EmailField(unique = True , null = True, blank=True)
    Address = models.CharField("Address :",max_length=100 , null=True, blank=True)
    Country = models.ForeignKey('Country',verbose_name="Country :" , on_delete=models.SET_NULL , null=True, blank=True)
    Currency = models.ForeignKey('Currency' ,verbose_name="Currency :" ,on_delete=models.SET_NULL , null=True, blank=True)
    Tax = models.ForeignKey('Tax' ,verbose_name="Tax :" ,on_delete=models.SET_NULL , null=True, blank=True)
    Cost_Method = models.IntegerField("Calculate item cost as :" ,choices=COSTMETH , null=True, blank=True)
    Create_Receive = models.BooleanField("Automaticlly create inter-store receive inventory orders :" , default=False)
    Create_Issue = models.BooleanField("Automaticlly create inter-store issue inventory orders :", default=False)
    Terms = models.TextField("Default Terms and Conditions :",null=True, blank=True) 
    WebsiteLink = models.URLField(max_length=200 , null = True, blank=True)
    WhatsappLink = models.URLField(max_length=200 , null = True, blank=True)
    FacebookLink = models.URLField(max_length=200 , null = True, blank=True)
    InstagramLink = models.URLField(max_length=200 , null = True, blank=True)
    CreatedDate = models.DateField(verbose_name="Created Date" , null=True)
    
    
    def __str__(self):
        return str(self.UserID)+'-'+str(self.OrganizationName)
    

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
    
    
class Country(models.Model):
    name = models.CharField(max_length=50 , null=True)
    
    def __str__(self):
        return self.name
    
    
    
class Currency(models.Model):
    name = models.CharField(max_length=50 , null=True)

    def __str__(self):
        return self.name
    
    
class Tax(models.Model):  
    pass

class UsersType(models.Model):
    UserTypeCode = models.IntegerField(null = True)
    UserTypeName = models.CharField(max_length=50 , null = True)
    
    def __str__(self):
        return self.UserTypeName
    
    
class Language(models.Model):
    language = models.CharField(max_length=50 , unique=True)
    
    def __str__(self):
        return self.language
    
    
