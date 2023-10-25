from django import forms
from .models import *

class TestForm2(forms.ModelForm):
    class Meta:
        model = TestApp
        fields = '__all__'