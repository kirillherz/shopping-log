from django.test import TestCase
from log.models import Product, CheckFromShop, Shop, Category
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

