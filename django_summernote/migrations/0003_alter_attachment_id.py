# Generated by Django 3.2.7 on 2022-02-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_summernote', '0002_update-help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
