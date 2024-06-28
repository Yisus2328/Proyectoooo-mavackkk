from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class TipoArte(models.Model):
    descripcion = models.CharField(max_length=60)

    def __str__(self):
        return self.descripcion

class Arte(models.Model):
    nombre = models.CharField(max_length=60)
    autor = models.CharField(max_length=60)
    tipo_arte = models.ForeignKey(TipoArte, on_delete=models.CASCADE)
    descripcion = models.CharField(default = "", max_length=200)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    dimensiones = models.CharField(max_length=60)
    correo_propietario = models.CharField(max_length=60)
    imagen = CloudinaryField('imagen')
    precio = models.PositiveIntegerField()
    validacion = False
    opciones = (
    ("aceptado", "Aceptado"),
    ("rechazado", "Rechazado"),
    ("pendiente", "Pendiente"),
    )

    estado = models.CharField(max_length=10,
                  choices=opciones,
                  default="pendiente")


    def __str__(self):
        return self.nombre
    

    

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Arte, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.usuario.username} - {self.producto.nombre} - {self.cantidad} - {self.precio_total}"