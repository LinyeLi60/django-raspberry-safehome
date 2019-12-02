# coding=utf-8
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate


# 首页
def home(request):
    return render(request, 'home.html', context={})


def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                print("登录成功!")
                request.session['is_login'] = True
                request.session['username'] = username
                return redirect('home')
            else:
                print("用户名或密码错误!")
                message = "Wrong user name or password!"

        return render(request, 'login.html', locals())

    login_form = LoginForm()
    message = 'Login'
    return render(request, 'login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return redirect("home")
    request.session.flush()
    return redirect(home)
