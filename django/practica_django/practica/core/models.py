from django.db import models

# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, null=True, blank=True, verbose_name="Apellido")
    edad = models.IntegerField(verbose_name="Edad")
    email = models.EmailField(verbose_name="Correo", blank=True, null=True)
    activo = models.BooleanField(verbose_name="Activo", default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    photo = models.ImageField(verbose_name="Foto de perfil", upload_to="media", blank=True, null=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ["nombre"]
    
    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)

# Relacion uno a uno
class Casa(models.Model):
    direccion = models.CharField(max_length=100, verbose_name="Direccion")
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)    

    def __str__(self):
        return self.direccion

# Relacion uno a mucho
class Telefono(models.Model):
    numero = models.IntegerField(verbose_name="Telefono")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="telefono")


# Relaciones muchos a muchos
class Curso(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre curso")
    persona = models.ManyToManyField(Persona)

# Segundo manera de ManyToMany
# class CursoPersona(models.Model):
#   curso = ForeignKey() 
#   persona = ForeignKey()
#   nota = IntegerFiel().....
    

# uno a uno -> OnetoOneField
# uno a mucho -> ForeignKey
# muchos a muchos -> ManyToManyField -> 1 y 2