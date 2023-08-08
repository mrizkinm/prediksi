from django.db import models

# Create your models here.

class Komoditas(models.Model):
    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama

class Harga(models.Model):
    date = models.DateField()
    harga = models.IntegerField()
    komoditas = models.ForeignKey(Komoditas, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.date)

class User(models.Model):
    nama = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=10)
    no_hp = models.CharField(max_length=20)

    def __str__(self):
        return self.nama

class Ramal(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    komoditas = models.ForeignKey(Komoditas, on_delete=models.CASCADE, null=True)
    model = models.CharField(max_length=10)
    start_train = models.DateField()
    end_train = models.DateField()
    start_ramal = models.DateField()
    end_ramal = models.DateField()
    mape_ramal = models.FloatField(null=True)
    rmse_ramal = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        super(Ramal, self).save(*args, **kwargs) 
        return self

    def __str__(self):
        return str(self.date)

class DetailRamal(models.Model):
    ramal = models.ForeignKey(Ramal, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    harga_aktual = models.FloatField(null=True)
    harga_ramal = models.FloatField(null=True)

    def __str__(self):
        return str(self.date)