# Generated by Django 4.2.2 on 2023-11-16 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_agenda_tarifa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='IdUsuario',
        ),
        migrations.AddField(
            model_name='box',
            name='IdAgenda',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.agenda'),
            preserve_default=False,
        ),
    ]
