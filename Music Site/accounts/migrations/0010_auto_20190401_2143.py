# Generated by Django 2.1.7 on 2019-04-01 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_user_rep'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rep',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='reputation',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reputs', to=settings.AUTH_USER_MODEL),
        ),
    ]
