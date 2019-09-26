# coding:utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator


def index(request):
    typelist = GoodType.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {'title': '首页', 'guest_cart':1,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, tid, pindex, sort):
    goodtype = GoodType.objects.get(pk=int(tid))
    news = goodtype.goodsinfo_set.order_by('-id')[0:2]
    # default method,order by id
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    # order by price
    elif sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('gprice')
    # order by click
    else:
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    # 开始分页
    paginator = Paginator(goods_list, 8)
    page = paginator.page(int(pindex))

    context = {'title': '商品列表', 'guest_cart': 1,
               'page': page, 'paginator': paginator,
               'goodtype': goodtype, 'sort': sort,
               'news': news}
    return render(request, 'df_goods/list.html', context)


def detail(request, id):
    good = GoodsInfo.objects.get(pk=int(id))
    good.gclick = good.gclick + 1
    good.save()
    news = good.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': '商品详情', 'guest_cart': 1,
               'good': good, 'news': news}
    return render(request, 'df_goods/detail.html', context)