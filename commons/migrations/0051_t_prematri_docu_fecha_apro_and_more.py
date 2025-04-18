# Generated by Django 5.1.4 on 2025-01-10 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0050_alter_t_prematri_docu_usr_apro'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='t_prematri_docu',
            name='fecha_apro',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_prematri_docu',
            name='fecha_carga',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='t_prematri_docu',
            name='usr_carga',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usrcarga', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='t_prematri_docu',
            name='usr_apro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aprobador', to=settings.AUTH_USER_MODEL),
        ),
    ]
