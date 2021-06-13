# Generated by Django 3.0.7 on 2021-06-13 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_perfil_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conquista',
            name='usuario',
        ),
        migrations.CreateModel(
            name='Conquista_Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conquista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Conquista')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
