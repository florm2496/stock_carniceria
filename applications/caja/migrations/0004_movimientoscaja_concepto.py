# Generated by Django 2.1.15 on 2021-03-16 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0003_concepto'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientoscaja',
            name='concepto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='caja.Concepto'),
        ),
    ]
