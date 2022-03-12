# Generated by Django 4.0.3 on 2022-03-12 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_client_latitude_client_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.gender'),
        ),
        migrations.AlterField(
            model_name='client',
            name='latitude',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='longitude',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
