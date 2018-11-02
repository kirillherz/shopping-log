from django.test import TestCase
from log.models import Product, CheckFromShop, Shop, Category, Day
from django.utils.timezone import now
from decimal import Decimal


class ProductTestCase(TestCase):

    def setUp(self):
        self.shop = Shop(name="test shop")
        self.shop.save()
        self.check = CheckFromShop(shop=self.shop, total=0, date=now())
        self.check.save()
        self.category = Category(name="test category", parent_category=None)
        self.category.save()
        self.product = Product(
            name="test product",
            cost=Decimal(15.0),
            checkFromShop=self.check,
            category=self.category)
        self.product.save()

    def test_create_product(self):
        product = Product.objects.get(name="test product")
        check = product.checkFromShop
        self.assertEqual(check.total, 15.0)

    def test_delete_product(self):
        product = Product.objects.get(name="test product")
        check = product.checkFromShop
        product.delete()
        self.assertEqual(check.total, 0)

    def test_update_product(self):
        product = Product.objects.get(name="test product")
        check = product.checkFromShop
        product.cost = 25
        product.save()
        self.assertEqual(check.total, 25)


class CheckFromShopTestCase(TestCase):

    def setUp(self):
        shop = Shop(name="test shop")
        shop.save()
        self.check = CheckFromShop(
            shop=shop,
            date=now(),
            total=Decimal(15.0))
        self.check.save()

    def test_create_check_from_shop(self):
        day = Day.objects.get(date=self.check.date)
        self.assertEqual(day.total, 15.0)

