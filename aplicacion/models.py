from django.db import models

#tipousuario si va
class TipoUsuario(models.Model):
    IdTipoUsuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

#usuario si va
class Usuario(models.Model):
    IdUsuario = models.AutoField(primary_key=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

#tipo producto si va
class TipoProducto(models.Model):
    IdTipoProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

#producto si va
class Producto(models.Model):
    IdProducto = models.AutoField(primary_key=True)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

#va en el examen
class Suscripcion(models.Model):
    IdSuscripcion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Suscripcion de {self.usuario.nombre}"

#va en el examen
class Compra(models.Model):
    IdCompra = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra {self.IdCompra} de {self.usuario.nombre}"

#va en el examen
class DetalleCompra(models.Model):
    IdDetalleCompra = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de compra {self.IdDetalleCompra} para compra {self.compra.IdCompra}"
    
    #separacion

class Promocion(models.Model):
    id_promocion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    descripcion = models.TextField()
    descuento = models.IntegerField()

    def str(self):
        return self.nombre
    class Meta:
        ordering = ['id_promocion']

        
    


