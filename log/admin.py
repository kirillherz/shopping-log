from django.contrib import admin
from log.models import Category, Product, CheckFromShop, Shop


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    pass


class CheckFromShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(CheckFromShop, CheckFromShopAdmin)

class ShopAdmin(admin.ModelAdmin):
    pass

admin.site.register(Shop, ShopAdmin)
