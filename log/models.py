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


