# Generated by Django 3.2.6 on 2021-08-15 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vmCreation', '0004_auto_20210815_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vmCreation.host'),
        ),
    ]
