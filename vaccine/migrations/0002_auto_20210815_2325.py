# Generated by Django 3.2.6 on 2021-08-15 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vaccine', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccinecard1',
            name='user',
        ),
        migrations.AddField(
            model_name='vaccinecard1',
            name='by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ha', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vaccinecard1',
            name='to_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='baby', to=settings.AUTH_USER_MODEL),
        ),
    ]