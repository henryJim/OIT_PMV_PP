from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class T_perfil(models.Model):
    class Meta:
        managed = True
        db_table = 'T_perfil'

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
        return f"{self.nombre} {self.apelli} - {self.get_gene_display()}"


class T_repre_legal(models.Model):
    class Meta:
        managed = True
        db_table = 'T_repre_legal'

    nom = models.CharField(max_length=200)
    tele = models.CharField(max_length=200)
    dire = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    paren = models.CharField(max_length=200)
    ciu = models.CharField(max_length=200)
    depa = models.CharField(max_length=200)


class T_instru(models.Model):
    class Meta:
        managed = True
        db_table = 'T_instru'

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
    class Meta:
        managed = True
        db_table = 'T_admin'
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Area/equipo: {self.area}"


class T_lider(models.Model):
    class Meta:
        managed = True
        db_table = 'T_lider'
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    area = models.CharField(max_length=200)
    esta = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Area/equipo: {self.area}"


class T_centro_forma(models.Model):
    class Meta:
        managed = True
        db_table = 'T_centro_forma'
    nom = models.CharField(max_length=100)
    dire = models.CharField(max_length=100)
    depa = models.CharField(max_length=100)
    muni = models.CharField(max_length=100)


class T_insti_edu(models.Model):
    class Meta:
        managed = True
        db_table = 'T_insti_edu'
    nom = models.CharField(max_length=100)
    dire = models.CharField(max_length=100)
    ofi = models.CharField(max_length=100)


class T_progra(models.Model):
    class Meta:
        managed = True
        db_table = 'T_progra'
    nom = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}"


class T_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 'T_ficha'
    fecha_aper = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    insti = models.ForeignKey(T_insti_edu, on_delete=models.CASCADE)
    centro = models.ForeignKey(T_centro_forma, on_delete=models.CASCADE)
    num = models.CharField(max_length=100)
    instru = models.ForeignKey(T_instru, on_delete=models.CASCADE)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)
    num_matri = models.CharField(max_length=100)


class T_fase_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 'T_fase_ficha'
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

    def __str__(self):
        return f"{self.fase}"


class T_crono(models.Model):
    class Meta:
        managed = True
        db_table = 'T_crono'
    nove = models.CharField(max_length=200)
    fecha_ini_acti = models.DateTimeField(null=True, blank=True)
    fecha_fin_acti = models.DateTimeField(null=True, blank=True)
    fecha_ini_cali = models.DateTimeField(null=True, blank=True)
    fecha_fin_cali = models.DateTimeField(null=True, blank=True)


class T_tipo_acti(models.Model):
    class Meta:
        managed = True
        db_table = 'T_tipo_acti'
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
        db_table = 'T_guia'
    nom = models.CharField(max_length=200)
    progra = models.ForeignKey(T_progra, on_delete=models.CASCADE)
    horas_auto = models.CharField(max_length=200)
    horas_dire = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}"


class T_acti(models.Model):
    class Meta:
        managed = True
        db_table = 'T_acti'
    nom = models.CharField(max_length=200)
    descri = models.CharField(max_length=500)
    horas_auto = models.CharField(max_length=200)
    horas_dire = models.CharField(max_length=200)
    tipo = models.ManyToManyField(T_tipo_acti)
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    fase = models.CharField(max_length=100)


class T_descri(models.Model):
    class Meta:
        managed = True
        db_table = 'T_descri'
    nom = models.CharField(max_length=200)


class T_acti_descri(models.Model):
    class Meta:
        managed = True
        db_table = 'T_acti_descri'
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)
    descri = models.ForeignKey(T_descri, on_delete=models.CASCADE)


class T_acti_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 'T_acti_ficha'
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)
    crono = models.ForeignKey(T_crono, on_delete=models.CASCADE)
    esta = models.CharField(max_length=200)


class T_apre(models.Model):
    class Meta:
        managed = True
        db_table = 'T_apre'
    ESTADO_ESTUDIANTE_CHOICES = [
        ('activo', 'Activo'),
        ('suspendido', 'Suspendido'),
        ('prematricula', 'Pre matricula')
    ]
    perfil = models.OneToOneField(T_perfil, on_delete=models.CASCADE)
    cod = models.CharField(max_length=200)
    esta = models.CharField(max_length=200, choices=ESTADO_ESTUDIANTE_CHOICES)
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    repre_legal = models.ForeignKey(T_repre_legal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.perfil.nombre} {self.perfil.apelli} - Ficha: {self.ficha}"


class T_acti_apre(models.Model):
    class Meta:
        managed = True
        db_table = 'T_acti_apre'
    apre = models.ForeignKey(T_apre, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti_ficha, on_delete=models.CASCADE)
    apro = models.CharField(max_length=200)
    fecha = models.DateTimeField(null=True, blank=True)


class T_encu(models.Model):
    class Meta:
        managed = True
        db_table = 'T_encu'
    fecha = models.DateTimeField(null=True, blank=True)
    lugar = models.CharField(max_length=200)
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)


class T_encu_apre(models.Model):
    class Meta:
        managed = True
        db_table = 'T_encu_apre'
    encu = models.ForeignKey(T_encu, on_delete=models.CASCADE)
    estu = models.ForeignKey(T_apre, on_delete=models.CASCADE)


class T_compe(models.Model):
    class Meta:
        managed = True
        db_table = 'T_compe'
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
        db_table = 'T_raps'
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
        return f"{self.nom} ({'Completado' if self.comple('Si') else 'Pendiente'})"


class T_rap_acti(models.Model):
    class Meta:
        managed = True
        db_table = 'T_rap_acti'
    rap = models.ForeignKey(T_raps, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)

    class Meta:
        db_table = 'T_rap_acti'


class T_crite_eva(models.Model):
    class Meta:
        managed = True
        db_table = 'T_crite_eva'
    crite = models.CharField(max_length=200)
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    evi = models.CharField(max_length=200)
    tecni = models.CharField(max_length=200)


class T_docu(models.Model):
    class Meta:
        managed = True
        db_table = 'T_docu'
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('eliminado', 'Eliminado'),
    ]
    nom = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    archi = models.FileField(upload_to='documentos/', null=True, blank=True)
    tama = models.CharField(max_length=200)
    priva = models.CharField(max_length=200)
    esta = models.CharField(
        max_length=200, choices=ESTADO_CHOICES, default='activo')


class T_guia_docu(models.Model):
    class Meta:
        managed = True
        db_table = 'T_guia_docu'
    guia = models.ForeignKey(T_guia, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)


class T_docu_proce(models.Model):
    class Meta:
        managed = True
        db_table = 'T_docu_proce'
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
        db_table = 'T_acti_docu'
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)
    acti = models.ForeignKey(T_acti, on_delete=models.CASCADE)


class T_recu(models.Model):
    class Meta:
        managed = True
        db_table = 'T_recu'
    nom = models.CharField(max_length=200)


class T_acti_recu(models.Model):
    class Meta:
        managed = True
        db_table = 'T_acti_recu'
    acti_docu = models.ForeignKey(T_acti_docu, on_delete=models.CASCADE)
    recu = models.ForeignKey(T_recu, on_delete=models.CASCADE)


class T_tipo_nove(models.Model):
    class Meta:
        managed = True
        db_table = 'T_tipo_nove'
    nom = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nom


class T_subtipo_nove(models.Model):
    class Meta:
        managed = True
        db_table = 'T_subtipo_nove'
    tipo = models.ForeignKey(
        T_tipo_nove, on_delete=models.CASCADE, related_name="subtipos")
    nom = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom}({self.tipo})"


class T_nove(models.Model):
    class Meta:
        managed = True
        db_table = 'T_nove'
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
        db_table = 'T_nove_docu'
    nove = models.ForeignKey(T_nove, on_delete=models.CASCADE)
    docu = models.ForeignKey(T_docu, on_delete=models.CASCADE)


class T_nove_ficha(models.Model):
    class Meta:
        managed = True
        db_table = 'T_nove_ficha'
    ficha = models.ForeignKey(T_ficha, on_delete=models.CASCADE)
    nove = models.ForeignKey(T_nove, on_delete=models.CASCADE)


class T_departa(models.Model):
    class Meta:
        managed = True
        db_table = 'T_departa'
    cod_departa = models.CharField(max_length=4, unique=True)
    nom_departa = models.CharField(max_length=200)

    def __str__(self):
        return self.nom_departa


class T_munici(models.Model):
    class Meta:
        managed = True
        db_table = 'T_munici'
    cod_munici = models.CharField(max_length=4, unique=True)
    nom_munici = models.CharField(max_length=200)
    nom_departa = models.ForeignKey(T_departa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_munici
