from django.contrib import admin

from medicines.models import Medicines, Suppliers, Stock, CustomerMedicine


@admin.register(Medicines)
class UserAdmin(admin.ModelAdmin):
    pass



@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerMedicine)
class CustomerMedicineAdmin(admin.ModelAdmin):
    pass
