# coding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import sha1
from models import *
from . import user_decorator


def register(request):
    context = {'title': '注册', 'mp': 'no-mp'}
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 验证两次密码是否相同
    if upwd != upwd2:
        return redirect('/user/register/')

    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    # 创建模型类对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    # 注册成功,转到登录页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    # 看看cookie有没有保存着用户名, cookie会随着http请求发送过来,所以在request里面取
    uname = request.COOKIES.get('uname', '')
    context = {'title': '登录', 'name_error': 0, 'pwd_error': 0, 'uname': uname,
               'mp': 'no-mp'}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember_username', 0)

    # 根据用户名查找对象
    # 用get,如果对象不存在,会抛异常,用try即可,filter会返回列表,不存在就返回空列表
    user = UserInfo.objects.filter(uname=uname)

    if len(user) == 1:
        # 说明用户名存在,开始匹配密码
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == user[0].upwd:
            # 正确,转到原本想去的页面, 从cookie拿,如果没有,就去首页吧,注意--> 因为我们要设置cookie,即还要读返回对象进行操作,redirect不行,所以不用redirect
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # 判断用户是否勾选了记住用户名
            if remember != 0:
                # 设置cookie
                red.set_cookie('uname', uname)
            else:
                # 也设置一个,设置为空
                red.set_cookie('uname', '', max_age=-1)
            # 把id和name存入sesssion
            request.session['user_id'] = user[0].id
            request.session['uname'] = uname
            return red
        else:
            # 错误, 转到原来页面,并提示消息
            context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'name_error': 0, 'pwd_error': 1}
            return render(request, 'df_user/login.html', context)
    else:
        # 说明用户名不存在
        context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'name_error': 1, 'pwd_error': 0}
        return render(request, 'df_user/login.html', context)


@user_decorator.login
def info(request):
    # 已经能保证数据存在了, 直接用get即可,不用担心抛异常
    uphone = UserInfo.objects.get(id=request.session['user_id']).uphone
    uaddress = UserInfo.objects.get(id=request.session['user_id']).uaddress
    uname = request.session['uname']
    if uphone == '':
        uphone = '未填写'
    if uaddress == '':
        uaddress = '未填写'
    context = {'title': '用户中心', 'page_name': 1, 'uname': uname, 'uphone': uphone, 'uaddress': uaddress}
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    context = {'title': '用户中心', 'page_name': 1}
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()

    uaddress = user.uaddress
    ushou = user.ushou
    uphone = user.uphone
    uyoubian = user.uyoubian
    if uaddress == '':
        uaddress = '未填写'
    context = {'title': '用户中心', 'page_name': 1, 'uaddress': uaddress, 'ushou': ushou, 'uyoubian': uyoubian, 'uphone': uphone}

    return render(request, 'df_user/user_center_site.html', context)

