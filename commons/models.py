from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
import os

class T_perfil(models.Model):
    class Meta:
        managed = True
        db_table = 't_perfil'

    GENERO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer')
    ]
    ROL_CHOICES = [
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('aprendiz', 'Aprendiz'),
        ('lider', 'Lider'),
        ('gestor', 'Gestor')
    ]
    DNI_CHOICES = [
        ('ti', 'Tarjeta de identidad'),
        ('cc', 'Cedula de ciudadania'),
        ('pp', 'Pasaporte'),
        ('cc', 'Tarjeta de extranjeria'),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    apelli = models.CharField(max_length=200)
    tipo_dni = models.CharField(max_length=50, choices=DNI_CHOICES, blank=True)
    dni = models.IntegerField()
    tele = models.CharField(max_length=100)
    dire = models.CharField(max_length=200)
    mail = models.EmailField(max_length=200)
    gene = models.CharField(max_length=20, choices=GENERO_CHOICES)
    fecha_naci = models.DateField(null=True, blank=True)
    rol = models.CharField(max_length=50, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.nom} {self.apelli} - {self.get_gene_display()}"

class T_repre_legal(models.Model):
    class Meta:
        managed = True
        db_table = 't_repre_legal'

    nom = models.CharField(max_length=200)
    dni = models.CharField(max_length=200)
    tele = models.CharField(max_length=200)
    dire = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    paren = models.CharField(max_length=200)
    ciu = models.CharField(max_length=200)
    depa = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nom}"

class T_instru(models.Model):
    class Meta:
        managed = True
        db_table = 't_instru'

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
        return f"{self.perfil.nom} {self.perfil.apelli} - Profesion: {self.profe}"

class T_admin(models.Model):
    class Meta:
        managed = True
        db_table = 't_admin'
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.perfil.nom} {self.perfil.apelli} - Area/equipo: {self.area}"
    
class T_lider(models.Model):
    class Meta:
        managed = True
        db_table = 't_lider'
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.perfil.nom} {self.perfil.apelli} - Area/equipo: {self.area}"

class T_gestor(models.Model):
    class Meta:
        managed = True
        db_table = 't_gestor'
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    perfil = models.ForeignKey(T_perfil, on_delete=models.CASCADE)
    esta = models.CharField(max_length=200, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.perfil.nom}"

class T_cuentas(models.Model):
    class Meta:
        managed = True
        db_table = 't_cuentas'
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    perfil = models.ForeignKey(T_perfil, on_delete = models.CASCADE)
    esta = models.CharField(max_length=100, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.perfil.nom} - Rol: Cuentas"
    
class T_departa(models.Model):
    class Meta:
        managed = True
        db_table = 't_departa'
    cod_departa = models.CharField(max_length=4, unique=True)
    nom_departa = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_departa

class T_gestor_depa(models.Model):
    class Meta:
        managed = True
        db_table = 't_gestor_depa'
    gestor = models.ForeignKey(T_gestor, on_delete=models.CASCADE)
    depa = models.ForeignKey(T_departa, on_delete=models.CASCADE)
    usuario_crea = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_crea = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.gestor} asignado al departamento {self.depa}"

class T_munici(models.Model):
    class Meta:
        managed = True
        db_table = 't_munici'
    cod_munici = models.CharField(max_length=10, unique=True)
    nom_munici = models.CharField(max_length=200)
    nom_departa = models.ForeignKey(T_departa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_munici

class T_centro_forma(models.Model):
    class Meta:
        managed = True
        db_table = 't_centro_forma'
    nom = models.CharField(max_length=50)
    cod = models.CharField(max_length=50)
    depa = models.ForeignKey(T_departa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom}"
    
class T_insti_edu(models.Model):
    class Meta:
        managed = True
        db_table = 't_insti_edu'
    SECTOR_CHOICES = [
        ('oficial', 'Oficial'),
        ('noficial', 'No oficial')
    ]
    ESTADO_CHOICES = [
        ('articulado', 'Articulado'),
        ('articulado nuevo', 'Articulado nuevo')
    ]
    dane = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    dire = models.CharField(max_length=100)
    secto = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    gene = models.CharField(max_length=100)
    zona = models.CharField(max_length=100)
    jorna = models.CharField(max_length=100)
    grados = models.CharField(max_length=100)
    num_sedes = models.CharField(max_length=100)
    esta = models.CharField(max_length=100, choices=ESTADO_CHOICES)
    cale = models.CharField(max_length=100)
    longi = models.CharField(max_length=100, blank=True, null=True)
    lati = models.CharField(max_length=100, blank=True, null=True)
    pote_apre = models.CharField(max_length=100, blank=True, null=True)
    muni = models.ForeignKey(T_munici, on_delete=models.CASCADE)
    vigen = models.CharField(max_length=100)
    recto = models.CharField(max_length=100, blank=True, null=True)
    recto_tel = models.CharField(max_length=100, blank=True, null=True)
    insti_mail = models.CharField(max_length=100, blank=True, null=True)
    coordi = models.CharField(max_length=100, blank=True, null=True)
    coordi_tele = models.CharField(max_length=100, blank=True, null=True)
    coordi_mail = models.CharField(max_length=100, blank=True, null=True)
    esta_docu = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.nom}"
    
class T_gestor_insti_edu(models.Model):
    class Meta:
        managed = True
        db_table = 't_gestor_insti_edu'
    gestor = models.ForeignKey(T_gestor, on_delete=models.CASCADE)
    insti = models.ForeignKey(T_insti_edu, on_delete=models.CASCADE)
    fecha_regi = models.DateTimeField(null=True, blank=True)
    esta = models.CharField(max_length=10)
    ano = models.CharField(max_length=10)
    seme = models.CharField(max_length=2)
    usuario_asigna = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gestor.perfil.nom} asociado a la intitucion {self.insti.nom}"
    
class T_progra(models.Model):
    class Meta:
        managed = True
        db_table = 't_progra'
    cod_prog = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    nomd = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}"

class T_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 't_ficha'
    fecha_aper = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    insti = models.ForeignKey(T_insti_edu, on_delete=models.CASCADE)
    centro = models.ForeignKey(T_centro_forma, on_delete=models.CASCADE)
    num = models.CharField(max_length=100)
    instru = models.ForeignKey(T_instru, on_delete=models.CASCADE)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)
    num_apre_proce = models.CharField(max_length=100)
    num_apre_forma = models.CharField(max_length=100)
    num_apre_pendi_regi = models.CharField(max_length=100)
    esta = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.num}"

class T_grupo(models.Model):
    class Meta:
        managed: True
        db_table = 't_grupo'
    insti = models.ForeignKey(T_insti_edu, on_delete=models.CASCADE)
    centro = models.ForeignKey(T_centro_forma, on_delete=models.CASCADE)
    num_apre_poten = models.CharField(max_length=5)
    esta = models.CharField(max_length=100)
    fecha_crea = models.DateTimeField()
    fecha_modi = models.DateTimeField(blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.insti}"

class T_gestor_grupo(models.Model):
    class Meta:
        managed: True
        db_table = 't_gestor_grupo'
    gestor = models.ForeignKey(T_gestor, on_delete=models.CASCADE)
    grupo = models.ForeignKey(T_grupo, on_delete=models.CASCADE)
    fecha_crea = models.DateTimeField()
    fecha_modi = models.DateTimeField(blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

class T_fase_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 't_fase_ficha'
    FASE_CHOICES = [
        ('fase analisis', 'Fase Analisis'),
        ('fase planeacion', 'Fase Planeacion'),
        ('fase ejecucion', 'Fase Ejecucion'),
        ('fase evaluacion', 'Fase Evaluacion'),
    ]
    fase = models.CharField(max_length=50, choices=FASE_CHOICES)
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    fecha_ini = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    instru = models.ForeignKey(T_instru, on_delete=models.CASCADE)
    vige = models.CharField(max_length=100, default='No')

    def __str__(self):
        return f"{self.fase}"

class T_crono(models.Model):
    class Meta:
        managed = True
        db_table = 't_crono'
    nove = models.CharField(max_length=200)
    fecha_ini_acti = models.DateTimeField(null=True, blank=True)
    fecha_fin_acti = models.DateTimeField(null=True, blank=True)
    fecha_ini_cali = models.DateTimeField(null=True, blank=True)
    fecha_fin_cali = models.DateTimeField(null=True, blank=True)

class T_tipo_acti(models.Model):
    class Meta:
        managed = True
        db_table = 't_tipo_acti'
    TIPO_CHOICES = [
        ('conocimiento', 'Conocimiento'),
        ('desempeño', 'Desempeño'),
        ('producto', 'Producto')
    ]
    tipo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tipo

class T_guia(models.Model):
    class Meta:
        managed = True
        db_table = 't_guia'
    nom = models.CharField(max_length=200)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)
    horas_auto = models.CharField(max_length=200)
    horas_dire = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}"

class T_acti(models.Model):
    class Meta:
        managed = True
        db_table = 't_acti'
    nom = models.CharField(max_length=200)
    descri = models.CharField(max_length=500)
    horas_auto = models.CharField(max_length=200)
    horas_dire = models.CharField(max_length=200)
    tipo = models.ManyToManyField(T_tipo_acti)
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    fase = models.CharField(max_length=100)
    raps = models.ManyToManyField('T_raps', related_name='acti', blank=True)

class T_descri(models.Model):
    class Meta:
        managed = True
        db_table = 't_descri'
    nom = models.CharField(max_length=200)

class T_acti_descri(models.Model):
    class Meta:
        managed = True
        db_table = 't_acti_descri'
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)
    descri = models.ForeignKey(T_descri, on_delete=models.CASCADE)

class T_acti_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 't_acti_ficha'
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)
    crono = models.ForeignKey(T_crono, on_delete=models.CASCADE)
    esta = models.CharField(max_length=200)

class T_apre(models.Model):
    class Meta:
        managed = True
        db_table = 't_apre'
    ESTADO_ESTUDIANTE_CHOICES = [
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('prematricula', 'Pre matricula')
    ]
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    cod = models.CharField(max_length=200)
    esta = models.CharField(max_length=200, choices=ESTADO_ESTUDIANTE_CHOICES)
    ficha = models.ForeignKey(T_ficha, on_delete= models.CASCADE, null=True, blank=True)
    grupo = models.ForeignKey(T_grupo, on_delete= models.CASCADE, null=True, blank=True)
    repre_legal = models.ForeignKey(T_repre_legal , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.perfil.nom} {self.perfil.apelli}"

class T_acti_apre(models.Model):
    class Meta:
        managed = True
        db_table = 't_acti_apre'
    apre = models.ForeignKey(T_apre, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti_ficha, on_delete=models.CASCADE)
    apro = models.CharField(max_length=200)
    fecha = models.DateTimeField(null=True, blank=True)

class T_encu(models.Model):
    class Meta:
        managed = True
        db_table = 't_encu'
    FASE_CHOICES = [
        ('fase analisis', 'Fase Analisis'),
        ('fase planeacion', 'Fase Planeacion'),
        ('fase ejecucion', 'Fase Ejecucion'),
        ('fase evaluacion', 'Fase Evaluacion'),
    ]
    fecha = models.DateTimeField(null=True, blank=True)
    tema = models.CharField(max_length=200)
    fase = models.CharField(max_length=200, choices=FASE_CHOICES)
    lugar = models.CharField(max_length=200)
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)

class T_encu_apre(models.Model):
    class Meta:
        managed = True
        db_table = 't_encu_apre'
    encu = models.ForeignKey(T_encu, on_delete=models.CASCADE)
    apre = models.ForeignKey(T_apre, on_delete= models.CASCADE)
    prese = models.CharField(max_length=200)
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)

class T_compe(models.Model):
    class Meta:
        managed = True
        db_table = 't_compe'
    FASE_CHOICES = [
        ('fase analisis', 'Fase Analisis'),
        ('fase planeacion', 'Fase Planeacion'),
        ('fase ejecucion', 'Fase Ejecucion'),
        ('fase evaluacion', 'Fase Evaluacion')
    ]
    nom = models.CharField(max_length=200)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)
    fase = models.CharField(max_length=200, choices=FASE_CHOICES)

    def __str__(self):
        return f"{self.nom} - Fase: {self.fase}"

class T_raps(models.Model):
    class Meta:
        managed = True
        db_table = 't_raps'
    FASE_CHOICES = [
        ('fase analisis', 'Fase Analisis'),
        ('fase planeacion', 'Fase Planeacion'),
        ('fase ejecucion', 'Fase Ejecucion'),
        ('fase evaluacion', 'Fase Evaluacion')
    ]
    nom = models.CharField(max_length=200)
    compe = models.ForeignKey(T_compe, on_delete=models.CASCADE)
    fase = models.CharField(max_length=100, choices=FASE_CHOICES)
    comple = models.CharField(max_length=100, default='No')

    def __str__(self):
        return f"{self.nom}"

class T_raps_ficha(models.Model):
    class Meta:
        managed= True
        db_table = 't_raps_ficha'
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    rap = models.ForeignKey(T_raps, on_delete=models.CASCADE)
    agre = models.CharField(max_length=100, default='No')

    def __str__(self):
        return f"RAP: {self.rap.nom} - Ficha: {self.ficha.num}"

class T_raps_acti(models.Model):
    class Meta:
        managed = True
        db_table = 't_raps_acti'
    rap = models.ForeignKey(T_raps, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)

class T_crite_eva(models.Model):
    class Meta:
        managed = True
        db_table = 't_crite_eva'
    crite = models.CharField(max_length=200)
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    evi = models.CharField(max_length=200)
    tecni = models.CharField(max_length=200)

def documentos(instance, filename):
    # Reemplazar espacios por guiones bajos y eliminar caracteres especiales
    nombre_base, extension = os.path.splitext(filename)
    nombre_base = nombre_base.replace(" ", "_")  # Reemplazar espacios
    nombre_base = "".join(c for c in nombre_base if c.isalnum() or c in ["_", "-"])  # Eliminar caracteres especiales
    return f'documentos/{nombre_base}{extension}'

class T_docu(models.Model):
    class Meta:
        managed = True
        db_table = 't_docu'
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('eliminado', 'Eliminado'),
    ]
    nom = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    archi = models.FileField(upload_to='documentos', null=True, blank=True, max_length=500 )
    tama = models.CharField(max_length=200)
    priva = models.CharField(max_length=200)
    esta = models.CharField(
        max_length=200, choices=ESTADO_CHOICES, default='activo')

class T_insti_docu(models.Model):
    class Meta:
        managed = True
        db_table = 't_insti_docu'
    nom = models.CharField(max_length=200)
    insti = models.ForeignKey(T_insti_edu, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_docu, on_delete=models.SET_NULL, blank=True, null=True)
    esta = models.CharField(max_length=200)
    vali = models.CharField(max_length=1, blank=True, null=True)
    usr_apro = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='documentos_insti_aprobados')
    fecha_apro = models.DateField(null=True, blank=True)
    usr_carga = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='documentos_insti_cargados')
    fecha_carga = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom}"

class T_prematri_docu(models.Model):
    class Meta:
        managed = True
        db_table = 't_prematri_docu'
    nom = models.CharField(max_length=200)
    apren = models.ForeignKey(T_apre, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_docu, on_delete=models.SET_NULL, blank=True, null=True)
    esta = models.CharField(max_length=200)
    vali = models.CharField(max_length=1, blank=True, null=True)
    usr_apro = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='documentos_aprobados')
    fecha_apro = models.DateField(null=True, blank=True)
    usr_carga = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='documentos_cargados')
    fecha_carga = models.DateField(null=True, blank=True)

class T_guia_docu(models.Model):
    class Meta:
        managed = True
        db_table = 't_guia_docu'
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)

class T_docu_proce(models.Model):
    class Meta:
        managed = True
        db_table = 't_docu_proce'
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    esta = models.CharField(max_length=200, choices=ESTADO_CHOICES)
    autor = models.CharField(max_length=200)
    publi = models.CharField(max_length=200)
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)

class T_acti_docu(models.Model):
    class Meta:
        managed = True
        db_table = 't_acti_docu'
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)

class T_recu(models.Model):
    class Meta:
        managed = True
        db_table = 't_recu'
    nom = models.CharField(max_length=200)

class T_acti_recu(models.Model):
    class Meta:
        managed = True
        db_table = 't_acti_recu'
    acti_docu = models.ForeignKey(T_acti_docu, on_delete=models.CASCADE)
    recu = models.ForeignKey(T_recu, on_delete=models.CASCADE)

class T_tipo_nove(models.Model):
    class Meta:
        managed = True
        db_table = 't_tipo_nove'
    nom = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nom

class T_subtipo_nove(models.Model):
    class Meta:
        managed = True
        db_table = 't_subtipo_nove'
    tipo = models.ForeignKey(
        T_tipo_nove, on_delete=models.CASCADE, related_name="subtipos")
    nom = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}({self.tipo})"

class T_nove(models.Model):
    class Meta:
        managed = True
        db_table = 't_nove'
    ESTADO_CHOICES = [
        ('creado', 'Creado'),
        ('gestion', 'En gestion'),
        ('resuelto', 'Resuelto')
    ]
    nom = models.CharField(max_length=200)
    descri = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.ForeignKey(T_tipo_nove, on_delete=models.PROTECT)
    sub_tipo = models.ForeignKey(T_subtipo_nove, on_delete=models.PROTECT)
    estado = models.CharField(max_length=200, choices=ESTADO_CHOICES)

class T_nove_docu(models.Model):
    class Meta:
        managed = True
        db_table = 't_nove_docu'
    nove = models.ForeignKey(T_nove, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)

class T_nove_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 't_nove_ficha'
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    nove = models.ForeignKey(T_nove, on_delete=models.CASCADE)

class T_DocumentFolder(MPTTModel):
    name = models.CharField(max_length=255) #Nombre de la carpeta o doc
    parent = TreeForeignKey('self', on_delete = models.CASCADE, null=True, blank=True, related_name='children')
    tipo = models.CharField(max_length=50, choices=[('documento', 'Documento'), ('link', 'Enlace'), ('carpeta', 'Carpeta')], default='carpeta')
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)
    iden = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class T_DocumentFolderAprendiz(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete = models.CASCADE, null=True, blank=True, related_name='children')
    tipo = models.CharField(max_length=50, choices=[('documento', 'Documento'), ('link', 'Enlace'), ('carpeta', 'Carpeta')], default='carpeta')
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    aprendiz = models.ForeignKey(T_apre, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)
    iden = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
class T_docu_labo(models.Model):
    class Meta:
        managed = True
        db_table = 't_docu_labo'
    CATEGORIA_CHOICES = [
        ('certificacion','Certificacion'),
        ('reconocimiento','Reconocimiento')
    ]
    usu = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    cate = models.CharField(max_length=100, choices=CATEGORIA_CHOICES)
    docu = models.ForeignKey(T_docu, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    esta = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.cate}"

class T_oferta(models.Model):
    class Meta:
        managed = True
        db_table = 't_oferta'
    TIPO_CONTRA_CHOICES =[
        ('terminoi', 'Termino Indefinido'),
        ('prestacion', 'Prestacion de servicios'),
        ('obra', 'Obra labor'),
        ('fijo', 'Termino fijo')
    ]
    JORNADA_CHOICES = [
        ('tiempoc','Tiempo completo'),
        ('horas','Por horas'),
        ('parcial','Tiempo parcial'),
    ]
    TIPO_CHOICES = [
        ('presencial','Presencial'),
        ('virtual','Virtual'),
        ('hibrido','Hibrido'),
    ]
    ESTADO_CHOICES = [
        ('creado','Creado'),
        ('publicado','Publicado'),
        ('cerrado','Cerrado'),
    ]
    nom = models.CharField(max_length=200)
    tipo_contra = models.CharField(max_length=200, choices=TIPO_CONTRA_CHOICES)
    jorna_labo = models.CharField(max_length=100, choices=JORNADA_CHOICES)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descri = models.TextField(max_length=3000)
    cargo = models.CharField(max_length=200)
    depa = models.ForeignKey(T_departa, on_delete=models.CASCADE)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)
    esta = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_ape = models.DateTimeField()
    fecha_cie = models.DateTimeField()
    edu_mini = models.CharField(max_length=200)
    expe_mini = models.CharField(max_length=200)
    profe_reque = models.CharField(max_length=100)
    usu_cre = models.ForeignKey(User, on_delete=models.CASCADE)

class T_oferta_instru(models.Model):
    class Meta:
        managed = True
        db_table = 't_oferta_instru'
    ofe = models.ForeignKey(T_oferta, on_delete=models.CASCADE)
    instru = models.ForeignKey(T_instru, on_delete=models.CASCADE)
    fecha_apli = models.DateTimeField(auto_now_add=True)
    esta = models.CharField(max_length=200)