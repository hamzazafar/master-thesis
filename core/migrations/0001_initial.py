# Generated by Django 2.1.4 on 2019-01-04 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_results', '0003_auto_20181106_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScanTimeSeriesResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('scan_name', models.CharField(max_length=255)),
                ('active_amplifiers_count', models.IntegerField()),
                ('scan_result', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='time_series_result', to='django_celery_results.TaskResult')),
            ],
        ),
    ]