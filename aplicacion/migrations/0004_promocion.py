# Generated by Django 5.0.6 on 2024-07-11 22:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0003_delete_modeloprueba'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id_promocion', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('descuento', models.IntegerField()),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion.producto')),
            ],
            options={
                'ordering': ['id_promocion'],
            },
        ),
    ]
