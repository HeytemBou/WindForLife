# Generated by Django 5.1.6 on 2025-02-17 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('anemometers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('wind_speed', models.FloatField()),
                ('unit', models.CharField(default='knots', max_length=10)),
                ('timestamp', models.DateTimeField()),
                ('anemometer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measurements', to='anemometers.anemometer')),
            ],
            options={
                'db_table': 'measurements',
            },
        ),
    ]
