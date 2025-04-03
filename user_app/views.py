from django.shortcuts import render,redirect
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from .forms import  *
import random
import time

# Create your views here.

class Registeration (View):
    def get(self,request):
        form = RegisterationForm()
        return render(request,'register.html',{'form':form})
    

    def post(self,request):
        otp=str(random.randint(1000,9999))
        
        request.session['user'] ={
            'username':request.POST['username'],
            'email':request.POST['email'],
            'first_name':request.POST['first_name'],
            'last_name':request.POST['last_name'],
            'password':request.POST['password'],
            'otp':otp,
            'time': time.time()}

        send_mail("OTP",f"Your OTP is {otp}","nevinbenedict07@gmail.com",[request.POST['email']],fail_silently=True)
        return redirect('otp')

class Otpverification(View):
    def get(self,request):
        form = OtpForm()
      
       
        return render(request,'otp.html',{'form':form})
    
    def post(self,request):
        form = OtpForm(request.POST)
        if form.is_valid():
            otp=form.cleaned_data.get('otp')
            user = request.session.get('user')
            if user.get('otp')==otp:
                if time.time()-user.get('time')<120:
                    User.objects.create_user(username=user.get('username'),email=user.get('email'),first_name=user.get('first_name'),last_name=user.get('last_name'),password=user.get('password'))
                    del request.session['user']
                    return redirect('register')         
                else:
                    del request.session['user']
                    return redirect('register')
            else:
                del request.session['user']
                return redirect('login') 

class Login(View):
    def get(self,request):
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self,request):
        form = LoginForm(request.POST)
    
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                print(request.user)
                return redirect('dashboard')
            else:
                print('Invalid credentials')
        
        return redirect('login')
    
class UserProfileView(View):
    def get (self,request):
        data=User.objects.get(id=request.user.id)
        return render(request,"user_details.html",{'data':data})

class Logout(View):
        def get(self,request):
            logout(request)
            return redirect('login')
        

class UserUpdate(View):
    def get (self,request):
        data=User.objects.get(id=request.user.id)
        form=UserUpdateForm(instance=data)
        return render(request,'userupdate.html',{'forms':form})
    

    def post(self,request):
        data=User.objects.get(id=request.user.id)
        form=UserUpdateForm(request.POST,instance=data)
        if form.is_valid:
            form.save()
        return redirect('dashboard')

