# Generated by Django 3.1.1 on 2020-09-28 09:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authtoken", "0002_auto_20160226_1747"),
    ]

    operations = [
        migrations.CreateModel(
            name="TokenProxy",
            fields=[],
            options={
                "verbose_name": "token",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("authtoken.token",),
        ),
    ]
