# Generated by Django 3.0.7 on 2020-07-18 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200711_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Foto de perfil'),
        ),
    ]