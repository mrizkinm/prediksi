# Generated by Django 4.0.2 on 2022-07-02 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bahanpokok', '0006_alter_harga_komoditas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harga',
            name='komoditas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bahanpokok.komoditas'),
        ),
    ]
