# Generated by Django 2.1.3 on 2019-06-08 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='time',
            new_name='poll_time',
        ),
        migrations.AddField(
            model_name='vote',
            name='poll_date',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
    ]
