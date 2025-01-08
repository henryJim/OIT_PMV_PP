# Generated by Django 5.1.4 on 2024-12-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0021_t_encu_fase_t_encu_tema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_encu',
            name='fase',
            field=models.CharField(choices=[('fase analisis', 'Fase Analisis'), ('fase planeacion', 'Fase Planeacion'), ('fase ejecucion', 'Fase Ejecucion'), ('fase evaluacion', 'Fase Evaluacion')], max_length=200),
        ),
    ]
