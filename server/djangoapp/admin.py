from django.contrib import admin
from .models import CarMake, CarModel

# Inline class to show CarModels inside CarMake
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# Admin class for CarMake with CarModel inline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    inlines = [CarModelInline]

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "type", "dealer_id", "year")
    list_filter = ("type", "car_make")
    search_fields = ("name", "dealer_id")

# Register models
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
