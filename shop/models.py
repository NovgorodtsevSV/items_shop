from django.db import models
from django.urls import reverse

from pytils.translit import slugify

# Create your models here.


class SlugifyMixin:
    slug_field = None

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.slug_field:
                source_value = getattr(self, self.slug_field, '')
                self.slug = slugify(source_value)
            else:
                raise ValueError("slug_field не определен")
        super().save(*args, **kwargs)
        
class TimeInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True

class Category(SlugifyMixin, TimeInfo):
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    category_name = models.CharField(max_length=200, unique=True, verbose_name='Название категории')
    
    slug_field = 'category_name'
    
    class Meta:
        ordering = ['category_name']
        verbose_name = 'Название категории'
        verbose_name_plural = 'Название категорий'
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.category_name
    
class Product(SlugifyMixin, TimeInfo):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категория товара')
    product_name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    #image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    slug_field = 'product_name'

    class Meta:
        ordering = ['product_name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'category_slug': self.category.slug, 'slug': self.slug})

    def __str__(self):
        return self.product_name
    
class ItemImage(TimeInfo, models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE, verbose_name='Изображение товара')
    image = models.ImageField(upload_to='products/images/', verbose_name='Изображение')
    is_primary = models.BooleanField(default=False, verbose_name='Основное изображение')

    def __str__(self):
        return f"Изображение для {self.product.product_name}"