# Generated by Django 4.2.2 on 2023-11-16 00:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_remove_box_idusuario_box_idagenda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='IdAgenda',
        ),
        migrations.AddField(
            model_name='box',
            name='IdUsuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
