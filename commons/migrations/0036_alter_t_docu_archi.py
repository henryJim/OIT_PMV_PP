# Generated by Django 5.1.4 on 2024-12-31 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0035_alter_t_documentfolder_iden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_docu',
            name='archi',
            field=models.FileField(blank=True, null=True, upload_to='renombrar_archivo'),
        ),
    ]
