# Generated by Django 3.2.3 on 2021-06-01 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0018_alter_post_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='chassis',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.IntegerField(),
        ),
    ]