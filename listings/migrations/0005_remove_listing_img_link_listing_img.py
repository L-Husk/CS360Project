# Generated by Django 5.1.7 on 2025-03-25 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_delete_ans_delete_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='img_link',
        ),
        migrations.AddField(
            model_name='listing',
            name='img',
            field=models.ImageField(blank=True, default='default.png', upload_to=''),
        ),
    ]
