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
               'request': request}
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
    # 点击量加一
    good = GoodsInfo.objects.get(pk=int(id))
    good.gclick = good.gclick + 1
    good.save()

    news = good.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': '商品详情', 'guest_cart': 1,
               'good': good, 'news': news}
    response = render(request, 'df_goods/detail.html', context)

    # 记录进最近浏览商品
    # 从cookies拿good_id, 如果是没有浏览记录的用户,就没有这个建，这时给个默认值即可
    good_ids = request.COOKIES.get('good_ids', '')
    good_id = str(good.id)
    # 如果是新用户，没有浏览记录, 直接写cookies即可
    if good_ids == '':
        good_ids = good_id
    # 如果里面已经有至少一条数据,
    else:
        # 拆分字符串，如果只有一个，也能用split
        good_ids_list = good_ids.split(',')
        # 如果该商品已经被记录了，那删除
        if good_ids_list.count(good_id) >= 1:
            good_ids_list.remove(good_id)
        # 添加数据
        good_ids_list.insert(0, good_id)
        # 如果记录的商品到达六个，就删除最后一个
        if len(good_ids_list) >= 6:
            del good_ids_list[5]
        # 通过逗号拼接列表为字符串
        good_ids = ','.join(good_ids_list)

    # 写入cookie
    response.set_cookie('good_ids', good_ids)
    return response
