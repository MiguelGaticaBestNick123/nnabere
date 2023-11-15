# Generated by Django 4.2.2 on 2023-11-15 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_pacientes_cell_alter_pacientes_direccion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloque',
            name='RutProfesional',
            field=models.ForeignKey(default=111111111, on_delete=django.db.models.deletion.CASCADE, related_name='RutProfesional_bloque', to='app.profesionales', verbose_name='Rut del profesional'),
            preserve_default=False,
        ),
    ]