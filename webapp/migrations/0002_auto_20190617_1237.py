# Generated by Django 2.2.2 on 2019-06-17 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignproduct',
            name='alert',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]