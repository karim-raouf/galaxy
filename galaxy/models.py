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
    ('Add-Ones' , 'Add-Ones'),
)

class User(AbstractUser):
    email = models.EmailField(unique = True)
    avatar = models.ImageField(null = True , default = 'avatar.svg')
    OrganizationID = models.ForeignKey( 'Organization' , on_delete=models.SET_NULL , null = True)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

class Organization(models.Model):
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    OrganizationName = models.CharField(max_length = 50 , null = True)
    CreatedDate = models.DateField(verbose_name="Created Date")
    
    def __str__(self):
        return self.OrganizationName
    



class Subscription(models.Model):
    
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    Status = models.BooleanField()
    StartDate = models.DateField(verbose_name="Start Date")
    EndDate = models.DateField(verbose_name="End Date")
    ProductID = models.ForeignKey('Product' , on_delete=models.SET_NULL , null=True)
    AutoRenew = models.BooleanField()
    Type = models.CharField(max_length=20 , choices=SUBTYPE , null=True)
    Bundle_T = models.CharField(max_length=20 , choices=BUNTYPE , null=True)
    
    def __str__(self):
        return str(self.ProductID)+'-'+str(self.UserID)
    
    

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
    
    
      

    
    




    

    

