# Generated by Django 5.1.7 on 2025-04-14 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maaun', '0004_remove_candidate_photo_candidate_avater'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='reg_no',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='year',
            field=models.IntegerField(max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='voter',
            name='level',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='voter',
            name='reg_no',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
