# Generated by Django 5.1.1 on 2024-11-10 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ انتشار'),
        ),
    ]
