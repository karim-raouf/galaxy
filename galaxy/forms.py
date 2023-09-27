from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.hashers import make_password
import re
        
class ProfileForm(forms.ModelForm):
    Birth_Date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}))
    avatar = forms.ImageField(widget=widgets.FileInput(attrs={'hidden': 'True'}) , required=False)
    
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
    
    GENDER = [
        ( 1 , 'Male'),
        ( 2 , 'Female'),
    ]
    
    
    Birth_Date = forms.DateField(widget=widgets.DateInput(attrs={'type': 'date'}) , required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'onfocus': 'showPswMsg()', 'onblur': 'hidePswMsg()', 'onkeyup': 'ChangePswMsgStatus(this.value)' , 'id': 'psw', 'name': 'psw' , 'placeholder':'Enter Password...'}))
    avatar = forms.ImageField(widget=widgets.FileInput(attrs={'hidden': 'True'}) , required=False)
    email = forms.EmailField(widget=widgets.EmailInput(attrs={'id': 'user-email', 'name': 'user-email' , 'placeholder' : 'Enter User\'s Email... '}))
    username = forms.CharField(widget=widgets.TextInput(attrs={'placeholder': 'Enter Username...'}))
    last_name = forms.CharField(widget=widgets.TextInput(attrs={'placeholder': 'Enter Last Name...'}))
    first_name = forms.CharField(widget=widgets.TextInput(attrs={'placeholder': 'Enter First Name...'}))
    Telephone = forms.CharField(widget=widgets.TextInput(attrs={'placeholder': 'Enter Telephone Number...'}) , required=False)
    Gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'gender-radio'}),choices=GENDER) 
    
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
        
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                self.instance = user
                if user.password:
                    self.fields['password'].required = False
            except User.DoesNotExist:
                pass

    def clean_password(self):
        # Validate the password field if it is not empty
        password = self.cleaned_data['password']
        if not password and self.fields['password'].required:
            raise forms.ValidationError("This field is required.")
        return password
    