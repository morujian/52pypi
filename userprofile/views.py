from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # 检测用户登录状态的装饰器
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.


# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            # 检验数据库中是否存在此用户，存在则返回user对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在session中，即实现了登录
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号密码输入有误")
        else:
            return HttpResponse("数据不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或者POST请求数据")


# 用户退出
def user_logout(request):
    logout(request)
    return redirect('article:article_list')


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("数据不合法")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("只支持POST和GET请求")


# 用户信息编辑
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("您无权限做此操作")
        profile_form = ProfileForm(request.POST, request.FILES)  # request.FILES文件类的数据
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:  # 为什么要做这样一个判断，因为，如果没有上传头像，不做判断的话，有可能会报错
                profile.avatar = profile_cd['avatar']
            profile.save()
            return redirect('userprofile:edit', id=id)
        else:
            return HttpResponse('提交的数据验证不合法')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'user': user, 'profile': profile}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('只接受POST和GET请求')





