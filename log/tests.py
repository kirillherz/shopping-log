from django.test import TestCase
from log.models import Product, CheckFromShop, Shop, Category, Day
from django.utils.timezone import now
from decimal import Decimal
from datetime import date


class ProductTestCase(TestCase):

    def setUp(self):
        shop = Shop(name="test shop")
        shop.save()
        check = CheckFromShop(shop=shop, total=0, date=now())
        check.save()
        category = Category(name="test category", parent_category=None)
        category.save()
        product = Product(
            name="test product",
            cost=Decimal(15.0),
            checkFromShop=check,
            category=category)
        product.save()

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
        check = CheckFromShop(
            shop=shop,
            date=date(2018, 2, 2),
            total=Decimal(15.0))
        check.save()

    def test_create_check_from_shop(self):
        day = Day.objects.get(date=date(2018, 2, 2))
        self.assertEqual(day.total, 15.0)

    def test_update_check_from_shop(self):
        check = CheckFromShop.objects.get(date=date(2018, 2, 2))
        check.total = Decimal(30.0)
        check.save()
        day = Day.objects.get(date=date(2018, 2, 2))
        self.assertEqual(day.total, Decimal(30.0))

    def test_delete_check_from_shop(self):
        day = Day.objects.get(date=date(2018, 2, 2))
        check = CheckFromShop.objects.get(date=date(2018, 2, 2))
        check.delete()
        day = Day.objects.get(date=date(2018, 2, 2))
        self.assertEqual(day.total, Decimal(0))
