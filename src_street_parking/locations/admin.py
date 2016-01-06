from django.contrib import admin

# Register your models here.
from .models import Location

class LocationAdmin(admin.ModelAdmin):
    class Meta:
        model = Location
        
admin.site.register(Location, LocationAdmin)
