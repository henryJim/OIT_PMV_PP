# Generated by Django 5.1.4 on 2024-12-22 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0020_t_acti_raps_delete_t_rap_acti'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_encu',
            name='fase',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='t_encu',
            name='tema',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
