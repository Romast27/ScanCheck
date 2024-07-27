from django.contrib import admin
from .models import Barcodes, Feedback


@admin.register(Barcodes)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name_product', 'category_name', 'brand_name')
    fields = ['barcode', 'name_product', 'category_name', 'brand_name']
    list_filter = ('category_name', 'brand_name')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id_barcode', 'text', 'time_creation', 'rating')
    fields = ['id_barcode', 'text', ('time_creation', 'rating')]
