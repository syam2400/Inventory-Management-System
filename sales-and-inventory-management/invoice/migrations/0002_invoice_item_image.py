# Generated by Django 4.2.6 on 2023-11-01 10:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='item_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='item_images/'),
            preserve_default=False,
        ),
    ]
