from django.contrib import admin

from .models import Car, Gas, Photo, Feature

# Register your models here.
admin.site.register(Car)
admin.site.register(Gas)
admin.site.register(Feature)

admin.site.register(Photo)