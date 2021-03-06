# Generated by Django 3.2 on 2021-04-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('openPrice', models.IntegerField(blank=True, null=True)),
                ('closePrice', models.IntegerField(blank=True, null=True)),
                ('highPrice', models.IntegerField(blank=True, null=True)),
                ('lowPrice', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
