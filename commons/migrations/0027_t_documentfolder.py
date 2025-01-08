# Generated by Django 5.1.4 on 2024-12-23 13:03

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0026_rename_estu_t_encu_apre_apre'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_DocumentFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('is_folder', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='commons.t_documentfolder')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
