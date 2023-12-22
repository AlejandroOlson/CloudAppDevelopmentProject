from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
admin.site.register(CarMake)
admin.site.register(CarModel)


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarMake, CarModel
    extra = 5

# CarModelAdmin class
# class CarModelAdmin(admin.ModelAdmin):
#     fields = ['name', 'dealer id', 'car type', 'year']
#     inlines = [CarModelInline]

# CarMakeAdmin class with CarModelInline
# class CarMakeAdmin(admin.ModelAdmin):
#     fields = ['name', 'description', 'year founded', 'country of origin']
#     inlines = [CarModelInline]

# Register models here
admin.site.register(CarModelInline)