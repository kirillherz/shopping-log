from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey(
        'self', blank=True,  null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Shop(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

class DayManager(models.Manager):
    def getDay(self,date):
        dayQyerySet = self.get_queryset().filter(date = date)
        if dayQyerySet.count():
            return dayQyerySet.get(date = date)
        else:
            return Day(total = 0, date = date)
            
class Day(models.Model):

    dayManager = DayManager()
    objects = models.Manager()
    date = models.DateField(unique=True)
    total = models.DecimalField(max_digits=15, decimal_places=2)


class CheckFromShop(models.Model):

    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    date = models.DateField()
    total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return "Чек из магазина " + self.shop.name

    def save(self, *args, **kwargs):
        dayQuerySet = Day.objects.filter(date=self.date)
        if dayQuerySet.count():
            day = dayQuerySet[0]
            if self.id == None:
                day.total += self.total
            else:
                old_checkFromShop = CheckFromShop.objects.get(pk=self.id)
                day.total -= old_checkFromShop.total
                day.total += self.total
            day.save()
        else:
            day = Day(date=self.date, total=self.total)
            day.save()
        super(CheckFromShop, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        day = Day.objects.get(date=self.date)
        day.total -= self.total
        day.save()
        super(CheckFromShop, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'


class Product(models.Model):

    name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    checkFromShop = models.ForeignKey(CheckFromShop, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.checkFromShop.total += self.cost
        else:
            old_product = Product.objects.get(pk=self.id)
            self.checkFromShop.total -= old_product.cost
            self.checkFromShop.total += self.cost
        self.checkFromShop.save()
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.checkFromShop.total -= self.cost
        self.checkFromShop.save()
        super(Product, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
