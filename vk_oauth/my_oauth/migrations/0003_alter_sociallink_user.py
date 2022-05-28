# Generated by Django 3.2.13 on 2022-05-24 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_oauth', '0002_rename_social_link_sociallink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sociallink', to=settings.AUTH_USER_MODEL),
        ),
    ]
