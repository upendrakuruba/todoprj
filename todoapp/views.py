from django.shortcuts import render,redirect
from django.contrib import auth,messages
# from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse

# Create your views here.


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        context = {'has_error':False,'data':request.POST}
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 3:
            messages.error(request,'Password must be at least 3 characters')
            return render(request,'register.html',context)
        
        if password!=password2:
            messages.error(request,'Password not match')
            return render(request,'register.html',context)
        

        if not username:
            messages.error(request,'Username Require')
            return render(request,'register.html',context)
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username Already Exists')
            return render(request,'register.html',context)
        

        if User.objects.filter(email=email).exists():
            messages.error(request,'Email Token')
            return render(request,'register.html',context)
        

        if context['has_error']:
            return render(request,'register.html',context)
        
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return redirect('login')
    return render(request,'register.html')


def Login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        context = {'data':request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)

        if user and not user.is_active:
            messages.error(request,'Email is not verified please check your email box')
            return render(request,'login.html')
        

        if not user:
            messages.error(request,'Invalid Credentials')
            return render(request,'login.html',context)
        
    
        login(request,user)
        return redirect('home')
        
    return render(request,'login.html')


def Logout_user(request):
    auth.logout(request)
    return redirect('login')



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            curren_site = get_current_site(request)
            email_subject = 'Reset your Password'
            message = render_to_string("reset_password_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Thankyou for registerring with us. we have send you a verification email to your email address. Please verify it.')
            return redirect('login')
 
        else:
            messages.error(request,'Account does not Exist')
            return redirect('forgotpassword')
    return render(request,'forgotpassword.html')



def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')



def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request,'resetpassword.html')
