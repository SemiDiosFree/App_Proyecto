# Generated by Django 2.1 on 2019-12-12 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import proyectos.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50, verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Etiqueta',
            },
        ),
        migrations.CreateModel(
            name='FotoTrampa',
            fields=[
                ('token', models.AutoField(primary_key=True, serialize=False)),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name='Dirección IP')),
                ('domain', models.URLField(blank=True, null=True, verbose_name='Dominio')),
            ],
            options={
                'verbose_name': 'Foto-Trampa',
                'verbose_name_plural': 'Foto-Trampas',
                'ordering': ['ipaddress'],
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Historial',
            },
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=proyectos.models.upload_location)),
            ],
            options={
                'verbose_name': 'Imágenes',
            },
        ),
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('content', models.TextField(verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('FKFT', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyectos.FotoTrampa', verbose_name='Foto-Trampa')),
                ('FKauthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('MTMIMG', models.ManyToManyField(blank=True, related_name='_proyectos_MTMIMG_+', to='proyectos.Imagenes', verbose_name='Imágenes')),
            ],
            options={
                'verbose_name': 'Proyecto',
            },
        ),
        migrations.CreateModel(
            name='Repositorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to=proyectos.models.upload_location)),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.Categorias', verbose_name='Etiqueta')),
            ],
            options={
                'verbose_name': 'Repositorio de imágenes',
            },
        ),
        migrations.AddField(
            model_name='imagenes',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyectos.Proyectos', verbose_name='idProyecto'),
        ),
        migrations.AddField(
            model_name='imagenes',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.Categorias', verbose_name='Etiqueta'),
        ),
        migrations.AddField(
            model_name='historial',
            name='idImages',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.Imagenes', verbose_name='Imagen'),
        ),
        migrations.AddField(
            model_name='historial',
            name='idPhotoTramp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.FotoTrampa', verbose_name='Foto-trampa'),
        ),
        migrations.AddField(
            model_name='historial',
            name='idProjecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.Proyectos', verbose_name='Projecto'),
        ),
        migrations.AddField(
            model_name='historial',
            name='idUser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
