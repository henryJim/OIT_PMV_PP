# Generated by Django 5.1.4 on 2024-12-22 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0022_alter_t_encu_fase'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_encu',
            name='ficha',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='commons.t_ficha'),
            preserve_default=False,
        ),
    ]
