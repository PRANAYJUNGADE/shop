# Generated by Django 4.2.4 on 2023-09-10 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_rename_category_categories_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter_price',
            name='price',
            field=models.CharField(choices=[('1000 To 10000', '1000 To 10000'), ('10000 To 20000', '10000 TO 20000'), ('20000 To 30000', '20000 TO 40000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000'), ('60000 TO 70000', '60000 TO 70000'), ('800000 TO 90000', '80000 TO 90000'), ('100000 TO 120000', '100000 TO 120000'), ('130000 TO 140000', '130000 TO 140000'), ('150000 TO 160000', '150000 TO 160000')], max_length=60),
        ),
    ]
