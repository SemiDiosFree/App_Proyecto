# Generated by Django 2.1 on 2019-12-12 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0007_auto_20191212_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenes',
            name='tag',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tag'),
        ),
    ]
