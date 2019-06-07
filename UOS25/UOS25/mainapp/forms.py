from django import forms
from mainapp.models import *

class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'mileage', 'gender', 'birthday', 'contact']

class StoreRegisterForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['id', 'address', 'contact', 'store_pay', 'store_code']
        widgets = {
            'id':forms.TextInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'contact':forms.TextInput(attrs={'class': 'form-control'}),
            'store_pay':forms.TextInput(attrs={'class': 'form-control'}),
            'store_code':forms.TextInput(attrs={'class': 'form-control'}),
        }
        

