# Generated by Django 3.2.13 on 2022-05-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='correlated_object',
            field=models.CharField(default='None', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='application',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='log',
            name='task_id',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
