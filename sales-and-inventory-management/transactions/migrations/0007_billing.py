# Generated by Django 4.2.6 on 2023-12-17 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_alter_sale_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_name', models.CharField(blank=True, max_length=20, null=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.sale')),
            ],
        ),
    ]
