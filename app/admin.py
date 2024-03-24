from django.contrib import admin
from .models import  *


@admin.register(Category)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','category_name']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','description', 'ingredient','price', 'product_image', 'created_at', 'unit']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']

