# Generated by Django 5.1.4 on 2024-12-25 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0034_t_documentfolder_iden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_documentfolder',
            name='iden',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
