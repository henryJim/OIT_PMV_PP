# Generated by Django 5.1.4 on 2025-01-26 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0080_alter_t_acti_table_alter_t_acti_apre_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_insti_edu',
            name='esta_docu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
