from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm
import json
from blog.models import *
# , ProfileUpdateForm

f = open('StockCode.json')
data=json.load(f)
CompanyNames=data.keys()

def register(request):
    # function which checks the details and gives access to register 
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            api=request.POST.get('api')
            Id=User.objects.filter(username=username)[0].id
            obj=AliceBlueApi(author_id=Id,alice_blue_api=api)
            obj.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register.html', {'form': form,'register':1,'CompanyNames':CompanyNames})


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid():
#             u_form.save()
#             # p_form.save()
#             messages.success(request, f'Your account has been updated')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         # p_form = ProfileUpdateForm(instance=request.user.profile)
        
#     context = {
#         'u_form': u_form,
#         # 'p_form': p_form
#     }
#     return render(request, 'profile.html', context)
