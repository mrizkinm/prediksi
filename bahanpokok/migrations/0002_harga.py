# Generated by Django 4.0.2 on 2022-06-22 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bahanpokok', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Harga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('harga', models.IntegerField()),
                ('komoditas_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bahanpokok.komoditas')),
            ],
        ),
    ]
