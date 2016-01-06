from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import ShowMap

class ShowMapAdmin(admin.ModelAdmin):
    class Meta:
        model = ShowMap
        
admin.site.register(ShowMap, ShowMapAdmin)
    