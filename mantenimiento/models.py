from django.db import models
from django.contrib.auth.models import User

class Vehiculo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # ...los demás campos que ya tenés...


# Create your models here.
class Vehiculo(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.PositiveIntegerField()
    tipo_combustible = models.CharField(max_length=30)
    color = models.CharField(max_length=30)

    foto_frontal = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_trasera = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_izquierda = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_derecha = models.ImageField(upload_to='vehiculos/', null=True, blank=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
    
class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    nombre = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    codigo = models.CharField(max_length=50, null=True, blank=True)
    marca = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.marca}) - ${self.precio_unitario}"
    
class Mantenimiento(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimiento, on_delete=models.PROTECT)
    fecha = models.DateField()
    proximo_mantenimiento = models.DateField(null=True, blank=True)
    repuestos = models.ManyToManyField(Repuesto, blank=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tipo.nombre.title()} - {self.vehiculo.placa} - {self.fecha}"

    
    def calcular_total(self):
        return sum(repuesto.precio_unitario for repuesto in self.repuestos.all())
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        total = self.calcular_total()
        if self.costo_total != total:
            self.costo_total
            super().save(update_fields=['costo_total'])


