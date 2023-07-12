import requests
from django.shortcuts import render,HttpResponse,redirect
from django import forms
from django.core.exceptions import ValidationError
from app01 import models
from app01.models import UserInfo
from app01.utils.encrypt import md5
import torch
from torch_model.run import Trainer
# Create your views here.

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput,
        required=True
    )
    confirm_password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput,
        required=True
    )
    mobile = forms.CharField(
        label='手机号',
        max_length=11,
        widget=forms.TextInput,
        required=True
    )
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = forms.ChoiceField(
        label='性别',
        widget=forms.RadioSelect,
        choices=gender_choices,
        required=True
    )
    birthdate = forms.DateField(
        label='出生日期',
        widget=forms.DateInput,
        required=True
    )
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if pwd != confirm :
            raise ValidationError("两次输入密码不一致")
        return confirm

class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput,
        required=True
    )



def index(request):
    info = request.session.get("info")
    username = info["username"]
    return render(request,'index.html',{'username':username})


def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'web.html',{'form':form})
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        print(request.POST)
        # form.save()
        username = request.POST['username']
        password = request.POST['password']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        birthdate = request.POST['birthdate']
        register_object = UserInfo.objects.filter(username=username).first()
        if register_object:
            form.add_error("username", "用户名已存在！")
            return render(request,'web.html',{'form':form})
        else:
            UserInfo.objects.create(username=username, password=md5(password), mobile=mobile,gender=gender,birthdate=birthdate)
            return redirect("/login/")
    return render(request,'web.html',{'form':form})

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        username = request.POST['username']
        password = request.POST['password']
        login_object = UserInfo.objects.filter(username=username, password=md5(password)).first()
        if not login_object:
            form.add_error("password","用户名或密码错误")
            return render(request,'login.html',{'form':form})
        request.session["info"] = {'username':login_object.username,'mobile':login_object.mobile}
        return redirect("/index/")
    return render(request,'login.html',{'form':form})

def userinfo(request):
    info = request.session.get("info")
    if not info:
        return render(request, 'login.html', {'form': form})
    username = info["username"]
    login_object = UserInfo.objects.filter(username=username).first()
    birthdate = login_object.birthdate
    gender = "男" if login_object.gender == 1 else "女"
    mobile = login_object.mobile
    return render(request,'userinfo.html',{"username":username,"gender":gender,"birthdate":birthdate,"mobile":mobile})

def upload(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    if request.method == 'GET':
        return render(request,'submit.html')
    username = info["username"]
    f = open('./userimg/'+username+'.tif',mode='wb')
    file_object = request.FILES.get('image')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    t = Trainer("./userimg", './torch_model/model.pt', './torch_model/model_{}_{}.pt', img_save_path=r'./app01/templates/static')
    t.segment(username+'.tif',username + '_result')
    return render(request, 'results.html',{"username":username})

def introduction(request):
    return render(request,'introduction.html')


