from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

'''class RegisterAdmin(admin.ModelAdmin):
    class Meta:
        models = Register

admin.site.register(Register,RegisterAdmin)

class RegisterEditInline(admin.StackedInline):
    model = RegistrationEdit
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = [RegisterEditInline, ]

admin.site.register(User, UserAdmin)
admin.site.register(User)'''
