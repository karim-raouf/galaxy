from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.hashers import make_password
        
class ProfileForm(forms.ModelForm):
    Birth_Date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'avatar' , 'email' , 'Language' , 'Telephone' , 'Gender' , 'Birth_Date']
        
        
class OrgForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['UserID' , 'SubscriptionID' , 'CreatedDate']
            
        
class AutoRenew(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['AutoRenew']
        
class SystemUserForm(forms.ModelForm):
    Birth_Date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}) , required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'onfocus': 'showPswMsg()', 'onblur': 'hidePswMsg()', 'onkeyup': 'ChangePswMsgStatus(this.value)' , 'id': 'psw', 'name': 'psw'}),
            required=False
    )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password)
        else:
            # Retrieve existing password from the database
            existing_user = User.objects.get(pk=user.pk)
            user.password = existing_user.password
        if commit:
            user.save()
        return user
    
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'avatar' , 'email' , 'Language' , 'Telephone' , 'Gender' , 'Birth_Date' , 'user_Type' , 'is_active' , 'password']