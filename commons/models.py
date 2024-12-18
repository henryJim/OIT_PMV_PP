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

class T_representante_legal(models.Model):
    nombre = models.CharField(max_length=200)
    tele = models.CharField(max_length=200)
    dire = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    paren = models.CharField(max_length=200)
    ciu = models.CharField(max_length=200)
    depa = models.CharField(max_length=200)

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

class T_centros_formacion(models.Model):
    nom = models.CharField(max_length=100)
    dire = models.CharField(max_length=100)
    depa = models.CharField(max_length=100)
    muni = models.CharField(max_length=100)

class T_instituciones_educativas(models.Model):
    nombre = models.CharField(max_length=100)
    dire = models.CharField(max_length=100)
    ofi = models.CharField(max_length=100)

class T_fichas(models.Model):
    fecha_aper = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    insti = models.ForeignKey(T_instituciones_educativas, on_delete= models.CASCADE)
    centro = models.ForeignKey(T_centros_formacion, on_delete= models.CASCADE)
    num = models.CharField(max_length=100)


class T_fases_ficha(models.Model):
    FASE_CHOICES = [
        ('fase analisis', 'Fase Analisis'),
        ('fase planeacion', 'Fase Planeacion'),
        ('fase ejecucion', 'Fase Ejecucion'),
        ('fase evaluacion', 'Fase Evaluacion'),
    ]
    fase = models.CharField(max_length=50, choices=FASE_CHOICES)
    ficha = models.ForeignKey(T_fichas, on_delete= models.CASCADE)
    fecha_ini = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    instru = models.ForeignKey(T_instructor, on_delete=models.CASCADE)

class T_cronogramas(models.Model):
    nove = models.CharField(max_length=200)
    fecha_ini_acti = models.DateTimeField(null=True, blank=True)
    fecha_fin_acti = models.DateTimeField(null=True, blank=True)
    fecha_ini_cali = models.DateTimeField(null=True, blank=True)
    fecha_fin_cali = models.DateTimeField(null=True, blank=True)

class T_programas(models.Model):
    nom = models.CharField(max_length=200)

class T_actividades(models.Model):
    TIPO_CHOICES = [
        ('conocimiento', 'Conocimiento'),
        ('desempeño', 'Desempeño'),
        ('producto', 'Producto')
    ]
    nom = models.CharField(max_length=200)
    horas_auto = models.CharField(max_length=200)
    horas_dire = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    progra = models.ForeignKey(T_programas, on_delete=models.CASCADE)

class T_descriptores(models.Model):
    nombre = models.CharField(max_length=200)

class T_actividades_descriptores(models.Model):
    acti = models.ForeignKey(T_actividades, on_delete=models.CASCADE)
    descri = models.ForeignKey(T_descriptores, on_delete=models.CASCADE)

class T_actividades_ficha(models.Model):
    ficha = models.ForeignKey(T_fichas, on_delete= models.CASCADE)
    acti = models.ForeignKey(T_actividades, on_delete=models.CASCADE)
    instru = models.ForeignKey(T_instructor, on_delete=models.CASCADE)
    crono = models.ForeignKey(T_cronogramas, on_delete=models.CASCADE)
    esta = models.CharField(max_length=200)

class T_aprendiz(models.Model):
    ESTADO_ESTUDIANTE_CHOICES = [
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('prematricula', 'Pre matricula')
    ]
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    cod = models.CharField(max_length=200)
    esta = models.CharField(max_length=200, choices=ESTADO_ESTUDIANTE_CHOICES)
    ficha = models.ForeignKey(T_fichas, on_delete= models.CASCADE)
    repre_legal = models.ForeignKey(T_representante_legal , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Ficha: {self.ficha}"

    
class T_actividades_aprendiz(models.Model):
    apre = models.ForeignKey(T_aprendiz, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_actividades_ficha, on_delete=models.CASCADE)
    apro = models.CharField(max_length=200)
    fecha = models.DateTimeField(null= True, blank=True)

class T_guias(models.Model):
    nom = models.CharField(max_length=200)
    progra = models.ForeignKey(T_programas, on_delete=models.CASCADE)
    horas_auto = models.CharField(max_length=200)
    horas_dire = models.CharField(max_length=200)

class T_encuentros(models.Model):
    fecha = models.DateTimeField(null=True, blank=True)
    lugar = models.CharField(max_length=200)
    guia = models.ForeignKey(T_guias, on_delete=models.CASCADE)

class T_encuentros_aprendiz(models.Model):
    encu = models.ForeignKey(T_encuentros, on_delete=models.CASCADE)
    estu = models.ForeignKey(T_aprendiz, on_delete= models.CASCADE)

class T_competencias(models.Model):
    FASE_CHOICES = [
        ('fase analisis', 'Fase Analisis'),
        ('fase planeacion', 'Fase Planeacion'),
        ('fase ejecucion', 'Fase Ejecucion'),
        ('fase evaluacion', 'Fase Evaluacion')
    ]
    nom = models.CharField(max_length=200)
    progra = models.ForeignKey(T_programas, on_delete=models.CASCADE)
    fase = models.CharField(max_length=200, choices= FASE_CHOICES)

class T_raps(models.Model):
    nom = models.CharField(max_length=200)
    compe = models.ForeignKey(T_competencias, on_delete=models.CASCADE)

class T_criterios_evaluacion(models.Model):
    crite = models.CharField(max_length=200)
    guia = models.ForeignKey(T_guias, on_delete=models.CASCADE)
    evi = models.CharField(max_length=200)
    tecni = models.CharField(max_length=200)

class T_documentos(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('eliminado', 'Eliminado'),
    ]
    nom = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    ruta = models.CharField(max_length=200)
    tama = models.CharField(max_length=200)
    priva = models.CharField(max_length=200)
    esta  = models.CharField(max_length=200)

class T_guias_documento(models.Model):
    guia = models.ForeignKey(T_guias, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_documentos, on_delete=models.CASCADE)

class T_documentos_proceso(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    esta = models.CharField(max_length=200, choices= ESTADO_CHOICES)
    autor = models.CharField(max_length=200)
    publi = models.CharField(max_length=200)
    docu = models.ForeignKey(T_documentos, on_delete=models.CASCADE)

class T_actividades_documento(models.Model):
    docu = models.ForeignKey(T_documentos, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_actividades, on_delete=models.CASCADE)

class T_recursos(models.Model):
    nom = models.CharField(max_length=200)

class T_actividades_recurso(models.Model): 
    acti_docu = models.ForeignKey(T_actividades_documento, on_delete=models.CASCADE)
    recu = models.ForeignKey(T_recursos, on_delete=models.CASCADE)

class T_novedades(models.Model):
    TIPO_CHOICES = [
        ('academico', 'Academico'),
        ('curriculo', 'Curriculo'),
        ('disciplinario', 'Disciplinario')
    ]
    ESTADO_CHOICES = [
        ('creado', 'Creado'),
        ('asignado', 'Asignado'),
        ('resuelto', 'Resuelto')
    ]
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)

class T_novedades_documentos(models.Model):
    nove = models.ForeignKey(T_novedades, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_documentos, on_delete=models.CASCADE)

class T_novedades_ficha(models.Model):
    ficha = models.ForeignKey(T_fichas, on_delete=models.CASCADE)
    nove = models.ForeignKey(T_novedades, on_delete=models.CASCADE)
