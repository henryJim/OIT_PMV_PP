# Generated by Django 5.1.4 on 2025-04-02 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0098_remove_t_documentfolder_iden_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_fase_ficha',
            name='instru',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commons.t_instru'),
        ),
    ]
