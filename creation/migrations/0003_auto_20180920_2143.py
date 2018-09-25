# Generated by Django 2.1.1 on 2018-09-20 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creation', '0002_auto_20180920_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('admin', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ManyToManyField(to='creation.User'),
        ),
    ]
