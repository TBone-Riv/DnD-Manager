# Generated by Django 3.1.5 on 2021-05-16 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master', to=settings.AUTH_USER_MODEL),
        ),
    ]
