# Generated by Django 5.2.3 on 2025-07-03 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_storage_company_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storage',
            old_name='company_id',
            new_name='company',
        ),
    ]
