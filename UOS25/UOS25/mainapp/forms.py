from django import forms
from mainapp.models import *

class StoreRegisterForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

    # Bootstrap CSS 적용
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'class':'form-control', 'placeholder' : field_name})
            self.fields[field_name].label = ''


class StoreUpdateForm(StoreRegisterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'id' : 'update_' + field_name})
        self.fields['store_id'].widget.attrs.update({'readonly' : True})

class StoreSearchForm(forms.Form):
    address = forms.CharField(max_length=80, required=False)
    contact = forms.CharField(max_length=20, required=False)
    store_pay_min = forms.DecimalField(min_value=0, required=False)
    store_pay_max = forms.DecimalField(max_value=1, required=False)

    # Bootstrap CSS 적용
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'class':'form-control', 'placeholder' : field_name})
            self.fields[field_name].label = ''

class SupplierRegisterForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

    # Bootstrap CSS 적용
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'class':'form-control', 'placeholder' : field_name})
            self.fields[field_name].label = ''

class SupplierUpdateForm(SupplierRegisterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'id' : 'update_' + field_name})
        self.fields['supplier_id'].widget.attrs.update({'readonly' : True})

class SupplierSearchForm(forms.Form):
    name = forms.CharField(max_length=25, required=False)
    contact = forms.CharField(max_length=20, required=False)
    email = forms.CharField(max_length=40, required=False)

    # Bootstrap CSS 적용
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'class':'form-control', 'placeholder' : field_name})
            self.fields[field_name].label = ''

class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    # Bootstrap CSS 적용
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'class':'form-control', 'placeholder' : field_name})
            self.fields[field_name].label = ''

class CustomerUpdateForm(CustomerRegisterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'id' : 'update_' + field_name})
        self.fields['customer_id'].widget.attrs.update({'readonly' : True})

class CustomerSearchForm(forms.Form):
    name = forms.CharField(max_length=25, required=False)
    mileage_min = forms.DecimalField(min_value=0, required=False)
    mileage_max = forms.DecimalField(min_value=0, required=False)
    gender = forms.DecimalField(required=False)
    birthday_min = forms.DateField(required=False)
    birthday_max = forms.DateField(required=False)
    contact = forms.CharField(max_length=20, required=False)

    # Bootstrap CSS 적용
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs.update({'class':'form-control', 'placeholder' : field_name})
            self.fields[field_name].label = ''