# Generated by Django 3.2.8 on 2022-11-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_refundagreement_date_of_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='actual_received_by',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
