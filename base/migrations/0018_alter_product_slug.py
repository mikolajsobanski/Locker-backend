# Generated by Django 4.1.1 on 2023-03-21 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_product_image_alter_product_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=models.CharField(blank=True, max_length=200, null=True), max_length=255),
        ),
    ]