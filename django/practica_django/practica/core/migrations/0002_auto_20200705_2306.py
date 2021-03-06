# Generated by Django 3.0.7 on 2020-07-05 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ['nombre'], 'verbose_name': 'Persona', 'verbose_name_plural': 'Personas'},
        ),
        migrations.AddField(
            model_name='persona',
            name='activo',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
        migrations.AddField(
            model_name='persona',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo'),
        ),
    ]
