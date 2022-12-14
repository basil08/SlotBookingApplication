# Generated by Django 4.1 on 2022-09-01 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0007_slot_frequency_slot_sport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='facility',
            field=models.ForeignKey(limit_choices_to={'sport': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.sport')}, on_delete=django.db.models.deletion.CASCADE, to='sport.facility'),
        ),
    ]
