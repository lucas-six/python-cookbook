# Generated by Django 3.2.15 on 2022-08-23 02:33

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('example_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='a',
            options={'verbose_name': 'A', 'verbose_name_plural': 'As'},
        ),
        migrations.AddField(
            model_name='a',
            name='age',
            field=models.PositiveSmallIntegerField(
                blank=True, null=True, verbose_name='age'
            ),
        ),
        migrations.AddField(
            model_name='a',
            name='balance',
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=8, verbose_name='balance'
            ),
        ),
        migrations.AddField(
            model_name='a',
            name='created_time',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='created time',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='a',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AddField(
            model_name='a',
            name='score',
            field=models.PositiveIntegerField(default=0, verbose_name='score'),
        ),
        migrations.AddField(
            model_name='a',
            name='sex',
            field=models.CharField(
                blank=True,
                choices=[('M', 'Man'), ('F', 'Female'), ('-', '-')],
                max_length=8,
                verbose_name='sex',
            ),
        ),
        migrations.AddField(
            model_name='a',
            name='sex2',
            field=models.CharField(
                blank=True,
                choices=[('Man', 'Man'), ('Female', 'Female'), ('-', '-')],
                max_length=8,
                verbose_name='sex',
            ),
        ),
        migrations.AddField(
            model_name='a',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time'),
        ),
        migrations.AddField(
            model_name='a',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid'
            ),
        ),
        migrations.AlterField(
            model_name='a',
            name='nickname',
            field=models.CharField(
                default='[unknown]', max_length=64, verbose_name='nickname'
            ),
        ),
        migrations.CreateModel(
            name='B',
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
                (
                    'a',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='example_app.a',
                        verbose_name='A',
                    ),
                ),
            ],
            options={
                'verbose_name': 'B',
                'verbose_name_plural': 'Bs',
            },
        ),
    ]
