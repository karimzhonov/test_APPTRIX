# Generated by Django 4.0.3 on 2022-03-12 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='latitude',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='longitude',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
