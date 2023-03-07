# Generated by Django 2.0.13 on 2023-02-27 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fam', models.CharField(default='P', max_length=40)),
                ('ka_fam', models.CharField(default='', max_length=40)),
                ('nam', models.CharField(default='V', max_length=40)),
                ('ka_nam', models.CharField(default='', max_length=40)),
                ('bkod', models.CharField(default='0-0-0', max_length=11)),
                ('addr', models.CharField(default='Klaipėda', max_length=50)),
                ('is_del', models.BooleanField(default=0)),
            ],
            options={
                'ordering': ('fam', 'nam'),
            },
        ),
        migrations.CreateModel(
            name='Dict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rword', models.CharField(default='', max_length=50)),
                ('lword', models.CharField(default='', max_length=50)),
            ],
            options={
                'ordering': ('rword',),
            },
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_ru', models.CharField(default='', max_length=10)),
                ('n_lt', models.CharField(default='', max_length=10)),
                ('ko_lt', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Works',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rwnam', models.CharField(default='', max_length=20)),
                ('lwnam', models.CharField(default='', max_length=50)),
            ],
            options={
                'ordering': ('rwnam',),
            },
        ),
        migrations.AddField(
            model_name='dict',
            name='wrk_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='spcapp.Works'),
        ),
    ]
