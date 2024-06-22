from django.db import models

class Monumetric(models.Model):
    seller_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    seller_type = models.CharField(max_length=100)
    date_first_added = models.DateField(auto_now_add=True)
    ad_platform = models.CharField(max_length=100, default='monumetric')

    class Meta:
        unique_together = ('domain', 'ad_platform')

class Mediavine(models.Model):
    seller_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    seller_type = models.CharField(max_length=100)
    date_first_added = models.DateField(auto_now_add=True)
    ad_platform = models.CharField(max_length=100, default='mediavine')

    class Meta:
        unique_together = ('domain', 'ad_platform')

class AdThrive(models.Model):
    seller_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    seller_type = models.CharField(max_length=100)
    date_first_added = models.DateField(auto_now_add=True)
    ad_platform = models.CharField(max_length=100, default='adthrive')

    class Meta:
        unique_together = ('domain', 'ad_platform')
