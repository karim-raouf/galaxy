from django import forms
from .models import *

        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'avatar']
        
        
class OrgForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['UserID' , 'SubscriptionID' , 'CreatedDate']
            
        
class AutoRenew(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['AutoRenew']
        