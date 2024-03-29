# Generated by Django 4.2.1 on 2023-06-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_alter_match_options_alter_player_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("GOAL", "Gol"),
                    ("OWNG", "Samobój"),
                    ("SHOT", "Strzał"),
                    ("FOUL", "Faul"),
                    ("YCAR", "Żółta kartka"),
                    ("RCAR", "Czerwona kartka"),
                    ("PENL", "Karny"),
                    ("GPEN", "Gol z karnego"),
                    ("OFFS", "Spalony"),
                    ("CRNR", "Rożny"),
                    ("FKCK", "Wolny"),
                    ("ASST", "Asysta"),
                ],
                max_length=4,
            ),
        ),
    ]
