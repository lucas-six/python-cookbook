# Generated by Django 3.2.15 on 2022-08-22 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                (
                    'nickname',
                    models.CharField(
                        default='unknown', max_length=64, verbose_name='nickname'
                    ),
                ),
            ],
        ),
    ]
