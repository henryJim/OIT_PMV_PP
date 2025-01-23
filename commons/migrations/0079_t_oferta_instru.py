# Generated by Django 5.1.4 on 2025-01-17 02:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0078_rename_decri_t_oferta_descri'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_oferta_instru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apli', models.DateTimeField(auto_now_add=True)),
                ('esta', models.CharField(max_length=200)),
                ('instru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.t_instru')),
                ('ofe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commons.t_oferta')),
            ],
            options={
                'db_table': 'T_oferta_instru',
                'managed': True,
            },
        ),
    ]
