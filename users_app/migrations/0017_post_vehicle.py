# Generated by Django 3.2.3 on 2021-05-31 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0016_post_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discussion', to='users_app.vehicle'),
        ),
    ]
