from django.contrib import admin
from .models import Product, Sale, Consumption

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'total_invested', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name', 'description')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_sold', 'amount', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')
    search_fields = ('product__name', 'description')

@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'amount_used', 'created_at', 'created_by')
    list_filter = ('created_at', 'created_by')
    search_fields = ('product__name', 'description')