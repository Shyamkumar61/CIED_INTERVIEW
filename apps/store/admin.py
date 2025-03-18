from django.contrib import admin
from apps.store.models import Medicine, Bill, BillItem, Category, Supplier

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    pass


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    pass


@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    pass
