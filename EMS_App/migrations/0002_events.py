# Generated by Django 4.2.17 on 2025-07-28 02:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EMS_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('startdate', models.DateTimeField(verbose_name='')),
                ('enddate', models.DateTimeField(verbose_name='')),
                ('location', models.CharField(max_length=200)),
                ('organizer', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Not Yet Started', 'Not Yet Started'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Not Yet Started', max_length=150)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
