# Generated by Django 5.0.6 on 2024-06-27 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='modeloprueba',
            fields=[
                ('modelocompraDetalleCompra', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
