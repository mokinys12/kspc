from django.conf import settings
from django.db import models
from django.utils import timezone


class Clients(models.Model):
    fam = models.CharField(max_length=40, default="P")
    ka_fam = models.CharField(max_length=40, default="")
    nam = models.CharField(max_length=40, default="V")
    ka_nam = models.CharField(max_length=40, default="")
    bkod = models.CharField(max_length=11, default="0-0-0")
    addr = models.CharField(max_length=50, default="Klaipėda")
    is_del = models.BooleanField(default=0)

    class Meta:
        ordering = ("fam", "nam")

    def __str__(self):
        return self.fam  # что будет отображаться в списке объектов этого класса


class Works(models.Model):
    rwnam = models.CharField(max_length=20, default="")
    lwnam = models.CharField(max_length=50, default="")

    class Meta:
        ordering = ("rwnam",)

    def __str__(self):
        return self.rwnam


class Dict(models.Model):
    rword = models.CharField(max_length=50, default="")
    lword = models.CharField(max_length=50, default="")
    wrk_type = models.ForeignKey(Works, default=0, on_delete=models.SET_DEFAULT)

    class Meta:
        ordering = ("rword",)

    def __str__(self):
        return self.rword


class Month(models.Model):
    n_ru = models.CharField(max_length=10, default="")
    n_lt = models.CharField(max_length=10, default="")
    ko_lt = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.n_ru
