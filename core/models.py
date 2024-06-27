from django.db import models

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
    imagen = models.ImageField(upload_to="arte", blank=True, null=False)
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
    

    

