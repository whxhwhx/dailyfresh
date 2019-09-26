from django.shortcuts import redirect
from django.http import HttpResponseRedirect


def login(func):
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())
            return red

    return login_fun


'''
http://127.0.0.1:8000/200/?type=10
request.path: ----> /200/
request.get_full_path: ----->/200/?type=10
'''