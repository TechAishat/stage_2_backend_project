from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    population = models.PositiveIntegerField(default=0)
    gdp = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    flag_image = models.ImageField(upload_to='flags/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'countries'
