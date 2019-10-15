# coding=utf-8
from django.shortcuts import render
from df_user.models import UserInfo
from df_cart.models import CartInfo
from django.shortcuts import redirect
from django.db import transaction
from df_user import user_decorator
from models import *
from datetime import datetime
from decimal import Decimal
from df_goods.models import GoodsInfo
from django.http import JsonResponse


@user_decorator.login
def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    ids = request.GET.getlist('card_id')
    if ids:
        # 成功取得card_id
        cart_list = []
        for card_id in ids:
            cart =CartInfo.objects.get(pk=int(card_id))
            # goods = GoodsInfo.objects.get(pk=int(cart.goods_id))
            # user = UserInfo.objects.get(pk=int(cart.user_id))
            cart_list.append(cart)

        # 通过card_id获得good信息，得到的信息传给模板，再拿到user信息，获取收货地址
        context = {"title": '提交订单', 'is_cart': 1, 'page_name': 1, 'cart_list': cart_list, 'user': user}
        return render(request, 'df_order/place_order.html', context)
    else:
        good_id = request.GET.get('good_id')
        good = GoodsInfo.objects.get(pk=int(good_id))
        context = {'title': '提交订单', 'page_name': 1, 'is_good': 1, 'user': user, 'good': good}
        return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    flag = request.POST.get('flag')
    if flag == '0':
        ids = request.POST.get('ids')
        try:
            # 创建订单对象
            order = OrderInfo()
            now = datetime.now()
            uid = request.session['user_id']
            order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
            order.user_id = uid
            order.odate = now
            order.ototal = Decimal(request.POST.get('total'))
            order.save()
            # 创建详单对象
            ids1 = [int(item) for item in ids.split(',')]
            for id in ids1:
                detail = OrderDetailInfo()
                # 之前是都是给id赋值，其实也可以直接用对象赋值即可
                detail.order = order
                # 拿到cart对象进行关联
                cart = CartInfo.objects.get(id=id)
                goods = cart.goods
                if goods.gkucun >= cart.count:
                    # 库存减去相应的数值
                    goods.gkucun = cart.goods.gkucun-cart.count
                    goods.save()
                    # 完善订单信息
                    detail.goods_id = goods.id
                    detail.price = goods.gprice
                    detail.count = cart.count
                    detail.save()
                    cart.delete()
                else:
                    transaction.savepoint_rollback(tran_id)
                    return redirect('/cart/')
            transaction.savepoint_commit(tran_id)

        except Exception as e:
            print '=======================%s' %e
            transaction.savepoint_rollback(tran_id)
            return JsonResponse({'success': 0})
        return JsonResponse({'success': 1})

    else:
        good_id = request.POST.get('id')
        try:
            # 创建订单对象
            order = OrderInfo()
            now = datetime.now()
            uid = request.session['user_id']
            order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
            order.user_id = uid
            order.odate = now
            order.ototal = Decimal(request.POST.get('total'))
            order.save()
            # 创建详单对象
            detail = OrderDetailInfo()
            # 之前是都是给id赋值，其实也可以直接用对象赋值即可
            detail.order = order
            # 拿到cart对象进行关联
            goods = GoodsInfo.objects.get(pk=int(good_id))
            if goods.gkucun >= 1:
                # 库存减去相应的数值
                goods.gkucun = goods.gkucun - 1
                goods.save()
                # 完善订单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = 1
                detail.save()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
            transaction.savepoint_commit(tran_id)

        except Exception as e:
            print '=======================%s' %e
            transaction.savepoint_rollback(tran_id)
            return JsonResponse({'success': 0})
        return JsonResponse({'success': 1})
