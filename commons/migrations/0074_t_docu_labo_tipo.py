# Generated by Django 5.1.4 on 2025-01-15 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0073_alter_t_docu_labo_cate'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_docu_labo',
            name='tipo',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
