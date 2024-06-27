from django.contrib import admin
from .models import * 
from admin_confirm import AdminConfirmMixin
from django.contrib.admin import ModelAdmin

class ArteModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre','descripcion','autor','tipo_arte','dimensiones','correo_propietario','imagen','precio']


class TipoModelAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['descripcion']


# Register your models here.
admin.site.register(TipoArte, TipoModelAdmin)
admin.site.register(Arte, ArteModelAdmin)