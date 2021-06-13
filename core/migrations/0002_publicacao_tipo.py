# Generated by Django 3.0.7 on 2021-06-08 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacao',
            name='tipo',
            field=models.IntegerField(choices=[(0, 'Comum'), (1, 'Empresas'), (2, 'Administrativa')], default=1),
            preserve_default=False,
        ),
    ]