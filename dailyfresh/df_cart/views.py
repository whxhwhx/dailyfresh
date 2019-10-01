# coding:utf-8
from django.shortcuts import render, redirect
from df_user import user_decorator
from models import CartInfo
from django.http import JsonResponse


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid).order_by('-id')
    context = {'title': '购物车', 'page_name': 1, 'carts': carts}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, minus, count):
    # 我们要拿到用户x买了y商品,用户， 就用session的user_id来解决， 商品，传过来id就行, 买了多少份，就用count
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)

    # 然后就可以查询数据库的值了，没有没关系，用filter，空的不会报错，只会返回空列表
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        if minus == '-':
            cart = carts[0]
            cart.count = cart.count - count
        else:
            cart = carts[0]
            cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count, 'number': cart.count})
    else:
        return redirect('/cart/')



@user_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)


@user_decorator.login
def edit(request, gid, count):
    # 我们要拿到用户x买了y商品,用户， 就用session的user_id来解决， 商品，传过来id就行, 买了多少份，就用count
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)

    # 然后就可以查询数据库的值了，没有没关系，用filter，空的不会报错，只会返回空列表
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
         cart = carts[0]
         cart.count = count
    cart.save()

    return JsonResponse({'number': cart.count})