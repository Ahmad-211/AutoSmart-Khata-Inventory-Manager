from django.contrib import admin
from .models import Customer, Part, Sale, SaleItem

# This makes the Sale items look nice inside the Sale page
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'current_balance', 'credit_limit')
    search_fields = ('name', 'phone')

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'oem_id', 'stock_qty', 'selling_price')
    list_filter = ('brand',)
    search_fields = ('name', 'oem_id')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'payment_type', 'timestamp')
    inlines = [SaleItemInline]