# Generated by Django 3.2.8 on 2022-09-14 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_leads_testing_appp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='accept_agreemnt',
        ),
    ]
