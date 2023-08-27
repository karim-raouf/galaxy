from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

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
    PlanID = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(3)])
    AutoRenew = models.BooleanField()
    OrganizationID = models.ForeignKey(Organization , on_delete=models.SET_NULL , null = True)
    
    def __str__(self):
        return self.UserID.email
    
    

class Account(models.Model):   
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    Balanace = models.DecimalField(max_digits=10, decimal_places=2)
    CreditLimit = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.UserID.email
    
    
class Cart(models.Model):
    UserID = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    ItemID = 
    Qty = 
    UnitPrice = 
    AddedDate = models.DateField(verbose_name="Added Date")
    
    




    

    

