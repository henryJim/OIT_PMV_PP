# Generated by Django 5.1.4 on 2025-01-12 00:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0059_remove_t_centro_forma_dire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_perfil',
            name='rol',
            field=models.CharField(choices=[('admin', 'Admin'), ('instructor', 'Instructor'), ('aprendiz', 'Aprendiz'), ('lider', 'Lider'), ('gestor', 'Gestor')], max_length=50),
        ),
        migrations.CreateModel(
            name='T_gestor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esta', models.CharField(max_length=200)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.t_perfil')),
            ],
            options={
                'db_table': 'T_gestor',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='t_insti_edu',
            name='gesto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commons.t_gestor'),
        ),
    ]
