# Generated by Django 5.1.2 on 2024-11-03 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='slary',
            new_name='salary',
        ),
    ]