# Generated by Django 5.1.4 on 2025-01-02 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("voteapp", "0008_candidate_thumbnail"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vote",
            old_name="Candidate",
            new_name="candidate",
        ),
    ]
