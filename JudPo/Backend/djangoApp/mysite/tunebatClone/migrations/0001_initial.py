# Generated by Django 4.0.5 on 2022-07-05 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insert',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('artist', models.CharField(blank=True, max_length=50)),
                ('genre', models.CharField(blank=True, max_length=25)),
                ('released_year', models.IntegerField(default=0)),
                ('song_key', models.CharField(blank=True, max_length=25)),
                ('bpm', models.IntegerField(default=0)),
                ('camelot', models.CharField(blank=True, max_length=3)),
                ('Instrumental_type', models.CharField(max_length=4)),
            ],
        ),
    ]