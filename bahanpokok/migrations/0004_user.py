# Generated by Django 4.0.2 on 2022-06-22 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bahanpokok', '0003_rename_komoditas_id_harga_komoditas'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=10)),
                ('no_hp', models.CharField(max_length=20)),
            ],
        ),
    ]
