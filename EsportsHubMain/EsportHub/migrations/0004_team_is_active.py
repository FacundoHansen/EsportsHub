# Generated by Django 4.2.5 on 2023-09-14 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EsportHub", "0003_alter_player_slug_alter_team_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]