# Generated by Django 5.0.4 on 2024-05-28 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_candidatura_id_alter_messaggio_id_utente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerta',
            name='luogo',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
