# Generated by Django 3.2.4 on 2021-06-23 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appusers', '0010_auto_20210623_0359'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_Follow', models.BooleanField(default=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_followed', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='follow_follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]