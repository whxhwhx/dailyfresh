from django.contrib import admin
from models import GoodType
from models import GoodsInfo


class GoodTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gtitle', 'gpic', 'gprice', 'gunit', 'gclick',
                    'gjianjie', 'gkucun', 'gcontent', 'gtype', 'gadv']


admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(GoodType, GoodTypeAdmin)

