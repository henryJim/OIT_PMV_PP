from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class T_perfil(models.Model):
    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ]
    ROL_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('aprendiz', 'Aprendiz'),
        ('lider', 'Lider')
    ]
    DNI_CHOICES = [
        ('ti', 'Tarjeta de identidad'),
        ('cc', 'Cedula de ciudadania'),
        ('pp', 'Pasaporte'),
        ('cc', 'Tarjeta de extranjeria'),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apelli = models.CharField(max_length=200)
    tipo_dni = models.CharField(max_length=50, choices=DNI_CHOICES, blank=True)
    dni = models.IntegerField()
    tele = models.CharField(max_length=100)
    dire = models.CharField(max_length=200)
    mail = models.EmailField(max_length=200)
    gene = models.CharField(max_length=20 , choices=GENERO_CHOICES)
    fecha_naci = models.DateField(null=True, blank=True)
    rol = models.CharField(max_length=50, choices=ROL_CHOICES)
    
    def __str__(self):
        return f"{self.nombre} {self.apelli} - {self.get_gene_display()}"

class T_instructor(models.Model):
    VINCULACION_CHOICES = [
        ('termino indefinido', 'Termino indefinido'),
        ('colaborador externo', 'Colaborador externo')
    ]
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    contra = models.CharField(max_length=200)
    fecha_ini = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    esta = models.CharField(max_length=200)
    profe = models.CharField(max_length=200)
    tipo_vincu = models.CharField(max_length=50, choices=VINCULACION_CHOICES)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Profesion: {self.profe}"

class T_aprendiz(models.Model):
    ESTADO_ESTUDIANTE_CHOICES = [
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('prematricula', 'Pre matricula')
    ]
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    cod = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)
    ficha = models.CharField(max_length=200)
    insti = models.CharField(max_length=200)
    repre_legal = models.CharField(max_length=200, choices=ESTADO_ESTUDIANTE_CHOICES)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Ficha: {self.ficha}"

class T_admin(models.Model):
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Area/equipo: {self.area}"
    
class T_lider(models.Model):
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Area/equipo: {self.area}"
    