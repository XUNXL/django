import requests
from django.contrib.auth import logout
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from django.core.exceptions import ValidationError
from app01 import models
from app01.models import UserInfo, UserLog, AdminInfo
from app01.utils.encrypt import md5
from my_functions.Predict import run_predict
from my_functions.calculate import calculate_age
import datetime
import shutil
# from torch_model.run import Trainer
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
        choices=gender_choices
    )
    birthdate = forms.DateField(
        label='出生日期',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_password')
        if pwd != confirm:
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


class AdminLoginForm(forms.Form):
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


def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'web.html', {'form': form})
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
            return render(request, 'web.html', {'form': form})
        else:
            UserInfo.objects.create(username=username, password=md5(
                password), mobile=mobile, gender=gender, birthdate=birthdate)
            return render(request, "reg.html")
    return render(request, 'web.html', {'form': form})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        username = request.POST['username']
        password = request.POST['password']
        login_object = UserInfo.objects.filter(
            username=username, password=md5(password)).first()
        if not login_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        request.session["info"] = {
            'username': login_object.username, 'mobile': login_object.mobile}
        return redirect("/introduction/")
    return render(request, 'login.html', {'form': form})


def userinfo(request):
    info = request.session.get("info")
    form = LoginForm()
    if not info:
        return render(request, 'login.html', {'form': form})
    username = info["username"]
    login_object = UserInfo.objects.filter(username=username).first()
    birthdate = login_object.birthdate
    gender = "♂" if login_object.gender == 1 else "♀"
    age = calculate_age(birthdate)
    mobile = login_object.mobile
    return render(request, 'index.html', {"username": username, "gender": gender, "birthdate": birthdate, "mobile": mobile, "age": age})


def upload(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    if request.method == 'GET':
        username = info["username"]
        return render(request, 'submit.html', {"username": username})
        # return redirect("/upload/")
    print("login")
    username = info["username"]
    f = open('./app01/static/images/'+username+'.jpg', mode='wb')
    file_object = request.FILES.get('image')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    print("process")
    probablistic, class_result, predict_entropy, max_mean_pro, n, bins = run_predict(
        "./app01/static/images/"+username +
        ".jpg", "./app01/static/images/"+username+"_normalize.jpg",
        "./app01/static/images/"+username+"_result.jpg")
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timesss = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    if predict_entropy > 0.5048 or max_mean_pro < 0.8:
        trust = 'distrust'
    else:
        trust = 'trust'
    UserLog.objects.create(username=username, logtime=time,
                           class_result=class_result, probablistic=probablistic, trust=trust, timesss=timesss)
    if class_result == 'Glaucoma':
        class_result = '您有比较大的概率患有青光眼，请及时前往医院就诊'
    elif class_result == 'Normal':
        class_result = '恭喜您，您的眼球健康状况良好'
    if trust == 'distrust':
        shutil.copy('./app01/static/images/' + username + '.jpg',
                    './app01/saveimg/distrust/' + username + timesss + '.jpg')
        return render(request, 'result.html', {"username": username, "time": time, "timesss": timesss, "x": bins, "y": n})
    else:
        shutil.copy('./app01/static/images/' + username + '.jpg',
                    './app01/saveimg/trust/' + username + timesss + '.jpg')
        return render(request, 'result.html',
                      {"username": username, "probablistic": round(probablistic, 4), "time": time, "timesss": timesss, "class_result": class_result, "x": bins, "y": n})
    # t = Trainer("./userimg", './torch_model/model.pt', './torch_model/model_{}_{}.pt', img_save_path=r'./app01/templates/static')
    # t.segment(username+'.tif',username + '_result')


def log_information(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login/")
    username = info["username"]
    print(username)
    queryset = UserLog.objects.filter(username=username).all()
    return render(request, 'userlog.html', {"queryset": queryset, "username": username})


def introduction(request):
    info = request.session.get("info")
    form = LoginForm()
    if not info:
        return render(request, 'login.html', {'form': form})
    username = info["username"]
    login_object = UserInfo.objects.filter(username=username).first()
    birthdate = login_object.birthdate
    gender = "♂" if login_object.gender == 1 else "♀"
    age = calculate_age(birthdate)
    mobile = login_object.mobile
    return render(request, 'introduction.html', {"username": username, "gender": gender, "birthdate": birthdate, "mobile": mobile, "age": age})


def my_logout(request):
    logout(request)
    return redirect("/login/")


def adminlogin(request):
    if request.method == 'GET':
        form = AdminLoginForm()
        return render(request, 'adminlogin.html', {'form': form})
    form = AdminLoginForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        username = request.POST['username']
        password = request.POST['password']
        login_object = AdminInfo.objects.filter(
            username=username, password=password).first()
        if not login_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'adminlogin.html', {'form': form})
        return redirect("/admin/")
    return render(request, 'adminlogin.html', {'form': form})


def admin(request):
    data_dict = {}
    value = request.GET.get('q')
    if value:
        data_dict['username'] = value
    queryset = UserLog.objects.filter(**data_dict)
    # if request.method == 'GET':
    #    queryset = UserLog.objects.all()
    return render(request, 'admin.html', {"queryset": queryset})


def result(request):
    info = request.session.get("info")
    username = info["username"]
    return render(request, 'result.html', {"username": username})
