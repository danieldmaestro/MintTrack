# Generated by Django 4.2.4 on 2023-09-06 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minttrack_app', '0004_alter_goal_target_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='start_date',
            field=models.DateField(auto_now=True),
        ),
    ]