from django.contrib import admin
from .models import Category, Product, ItemImage

# Register your models here.


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name',]
    exclude = ['slug']
    #prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'available', 'created', 'updated']
    exclude = ['slug']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    
    inlines = [ItemImageInline, ]
    #prepopulated_fields = {'slug': ('name',)}

# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     inlines = [ItemImageInline]
#     prepopulated_fields = {'slug': ('name',)}