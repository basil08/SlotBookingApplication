# Generated by Django 4.1 on 2022-08-31 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0004_slot_created_at_slot_created_by_slot_last_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='name',
            field=models.CharField(default='Mittal Sports Complex Basketball Court', max_length=300),
            preserve_default=False,
        ),
    ]
