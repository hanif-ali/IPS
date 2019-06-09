# Generated by Django 2.1.3 on 2019-05-29 07:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slogan', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('level', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('motto', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=2)),
                ('active', models.BooleanField()),
                ('candidates', models.ManyToManyField(to='vote.Candidate')),
                ('grade', models.ForeignKey(on_delete=None, to='vote.Grade')),
                ('house', models.ForeignKey(on_delete=None, to='vote.House')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('grade', models.ForeignKey(on_delete=None, to='vote.Grade')),
                ('user', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('candidate', models.ForeignKey(on_delete=None, to='vote.Candidate')),
                ('poll', models.ForeignKey(on_delete=None, to='vote.Poll')),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='voted',
            field=models.ManyToManyField(blank=True, to='vote.Student'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='student',
            field=models.ForeignKey(on_delete=None, to='vote.Student'),
        ),
    ]
