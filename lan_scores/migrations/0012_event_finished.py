# Generated by Django 5.2 on 2025-04-23 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lan_scores', '0011_alter_scores_game_instance'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
