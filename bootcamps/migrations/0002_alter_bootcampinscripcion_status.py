# Generated by Django 4.1.4 on 2023-04-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootcamps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootcampinscripcion',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Aprroved'),
        ),
    ]
