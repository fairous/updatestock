from django.contrib import admin
from . forms import *

from . models import Stock, Bike, Brand


class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'bike_name', 'part_number', 'part_name', 'mrp_amount', 'exchange_rate',
                    'shipping_amount', 'cost', 'margine', 'add', 'quantity', 'receive_quantity', 'receive_by',
                    'issue_quantity', 'issue_by', 'issue_to', 'created_by', 'reorder_level', 'export_to_CSV']
    form = StockCreateForm
    list_filter = ['brand_name', 'bike_name']
    search_fields = ['bike_name', 'part_name']


# Register your models here.
admin.site.register(Brand)
admin.site.register(Bike)
admin.site.register(Stock, StockCreateAdmin)


from django.contrib import admin
from .models import Invoice
from .forms import InvoiceForm


# Register your models here.

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'invoice_number', 'invoice_date', 'line_one_bike_name']
    form = InvoiceForm
    list_filter = ['name']
    search_fields = ['name', 'invoice_number']


admin.site.register(Invoice, InvoiceAdmin)

