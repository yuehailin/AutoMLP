# Generated by Django 2.0 on 2019-09-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('task_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('csv_path', models.CharField(max_length=512)),
                ('yaml_path', models.CharField(max_length=512)),
                ('up_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('kind', models.CharField(max_length=128, unique=True)),
                ('describe', models.CharField(max_length=128, unique=True)),
                ('filename', models.CharField(max_length=128, unique=True)),
                ('filecreatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('csv_path', models.CharField(max_length=512)),
                ('yaml_path', models.CharField(max_length=512)),
                ('up_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]