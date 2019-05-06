from django.forms import ModelForm
from mainapp.models import *

class Form(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'content']