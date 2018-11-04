from django.contrib import admin
from log.models import Category, Product, CheckFromShop, Shop, Day


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):

    def delete_queryset(self, request, queryset):
        for product in queryset:
            product.checkFromShop.total -= product.cost
            product.checkFromShop.save()
        queryset.delete()


admin.site.register(Product, ProductAdmin)


class CheckFromShopAdmin(admin.ModelAdmin):

    def delete_queryset(self, request, queryset):
        for check in queryset:
            day = Day.objects.get(date=check.date)
            if CheckFromShop.objects.filter(date = check.date).count() > 1:
                day.total -= check.total
                day.save()
            else:
                day.delete()
        queryset.delete()


admin.site.register(CheckFromShop, CheckFromShopAdmin)


class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)
