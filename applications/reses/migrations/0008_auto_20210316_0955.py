# Generated by Django 2.1.15 on 2021-03-16 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reses', '0007_auto_20210315_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res',
            name='nombre',
            field=models.CharField(default='Res', max_length=20),
        ),
    ]
