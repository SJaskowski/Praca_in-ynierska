# Generated by Django 3.0.2 on 2020-01-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Witryna', '0002_remove_produkt_etykieta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kategoria',
            name='id',
            field=models.CharField(max_length=3, primary_key=True, serialize=False),
        ),
    ]