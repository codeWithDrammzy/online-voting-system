# Generated by Django 5.2.1 on 2025-05-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maaun', '0005_alter_candidate_reg_no_alter_election_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='year',
            field=models.IntegerField(),
        ),
    ]
