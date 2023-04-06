from django.db import models

class Mesaj(models.Model):
    ad = models.CharField('ad: ', max_length=25)
    email = models.CharField('email: ', max_length=25)
    movzu = models.CharField('movzu: ', max_length=15)
    mesaj = models.CharField('mesaj ', max_length=200)
    Tarix = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.ad
    def get_absolute_url(self):
        return f'/'

class Koment(models.Model):
    ad = models.CharField('ad: ', max_length=25)
    email = models.CharField('email: ', max_length=25)
    movzu = models.CharField('movzu: ', max_length=15)
    mesaj = models.CharField('mesaj: ', max_length=165)
    cari_id =models.IntegerField('cari_xeber: ', max_length=10)
    Tarix = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.ad
    def get_absolute_url(self):
        return f'/'


class Newsdata(models.Model):
    link= models.CharField(max_length=50)
    basliq= models.CharField(max_length=100)
    foto= models.CharField(max_length=1000)
    metn= models.CharField(max_length=1000)
    kateqoriya = models.CharField(max_length=25)
    tarix= models.CharField(max_length=25)

    
    def __str__(self):
        return self.basliq
    def get_absolute_url(self):
        return f'/'





class Newsdata(models.Model):
    link= models.CharField(max_length=50)
    basliq= models.CharField(max_length=100)
    foto= models.CharField(max_length=1000)
    metn= models.CharField(max_length=1000)
    kateqoriya = models.CharField(max_length=25)
    tarix= models.CharField(max_length=25)

    
    def __str__(self):
        return self.basliq
    def get_absolute_url(self):
        return f'/'