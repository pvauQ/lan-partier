# Generated by Django 5.2 on 2025-04-10 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lan_scores', '0007_alter_game_link_alter_gameinstance_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinstance',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lan_scores.game'),
        ),
    ]
