# Generated by Django 4.1.1 on 2022-09-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_product_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('New', 'Nowy'), ('New', 'Używany'), ('New', 'Uszkodzony')], default='provide', max_length=14),
        ),
    ]
