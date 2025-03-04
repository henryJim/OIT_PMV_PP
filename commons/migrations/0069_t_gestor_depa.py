# Generated by Django 5.1.4 on 2025-01-14 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0068_alter_t_insti_docu_docu'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_gestor_depa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.t_departa')),
                ('gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.t_gestor')),
            ],
            options={
                'db_table': 'T_gestor_depa',
                'managed': True,
            },
        ),
    ]
