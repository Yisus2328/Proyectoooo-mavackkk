from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

# CONFIGURACION PARA EL API
router = routers.DefaultRouter()
router.register('tipoartes', TipoArteViewset)
router.register('artes', ArteViewset)


urlpatterns = [
    

    path('agregar_al_carrito/<int:arte_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar_carrito/', vaciar_carrito, name='vaciar_carrito'),

    path('registrar_compra/', registrar_compra, name='registrar_compra'),
    path('historia_compras/', historia_compras, name='historia_compras'),

    path('voucher/', voucher, name="voucher"),
    path('', visualizar, name="index"),
    path('detalle_producto/', listados, name="producto"),
    path('solicitudes/', solicitudes, name="solicitudes"),
    path('Edvardmun/', Edvardmun, name="Edvardmun"),
    path('VanGoh/', VanGoh, name="VanGoh"),
    path('Leonardo/', Leonardo, name="Leonardo"),
    path('pago/', pago, name="pago"),
    path('exitoso/',exitoso, name="exitoso"),
    
    path('aceptado/<int:id>/',aceptado, name='aceptado'),
    path('rechazado/<int:id>/',rechazado, name='rechazado'),

    # CRUD
    path('detalle_producto/add/', arteadd, name="add"),
    path('update/<int:id>/', arteupdate, name="update"),
    path('detalle_producto/delete/<int:id>/', artedelete, name="delete"),

    #register
    path('register/', register, name="register"),

    #account locked
    path('account_locked/', account_locked, name="account_locked"),


    #API
    path('api/', include(router.urls)),
    path('artesapi/', artesapi, name="artesapi"), 
    path('artedetalle/<id>/', artedetalle, name="artedetalle"), 
    


]
