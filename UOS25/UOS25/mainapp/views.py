from django.shortcuts import render
from mainapp.forms import *

# Create your views here.

def index(request):
    return render(request, 'index.html')
    
def registerProduct(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = Form()
    return render(request, 'registerProduct.html', {'form':form})

    