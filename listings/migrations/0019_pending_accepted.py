# Generated by Django 4.2.20 on 2025-04-17 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0018_alter_partnerrequest_inputuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='pending',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
