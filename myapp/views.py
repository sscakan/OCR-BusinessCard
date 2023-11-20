from django.shortcuts import render
from . import arg
from myapp.models import Information
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.
def upload(request):
    if request.method == 'POST':
        images_list = request.FILES.getlist('images')
        for image in images_list:
            info = arg.image_processing(image)
            phone = arg.phone_check(info)
            web = arg.web_check(info)
            company = arg.company_check(info,web)
            mail = arg.mail_check(info)
        
            information = Information(company=company,phone=phone,web=web,mail=mail,unclassified=info)
            
            
            try:
                information.save()
                messages.success(request, 'The business card has been added to the database successfully.')
            except IntegrityError:
                messages.warning(request, 'The business card already exists in the database.')
            except: 
                messages.warning(request, 'Error occured during uploading: Check your file.')
                
                
    return render(request,'upload.html')

def welcome(request):
    return render(request,'welcome.html')