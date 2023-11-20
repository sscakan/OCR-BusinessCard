# Generated by Django 3.2.7 on 2023-08-21 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=355, unique=True)),
                ('web', models.CharField(max_length=255)),
                ('mail', models.CharField(max_length=355)),
                ('unclassified', models.CharField(max_length=355)),
            ],
        ),
    ]