from django.db import models


class market_source_data_ats(models.Model):
    id = models.BigAutoField(primary_key=True)
    observation_date = models.DateTimeField()
    publication_date = models.DateTimeField(default=None, blank=True, null=True)
    price_zone_code = models.IntegerField()
    consumer_price = models.DecimalField(max_digits=20, decimal_places=6)
    consumer_volume = models.DecimalField(max_digits=20, decimal_places=6)
    thermal_volume = models.DecimalField(max_digits=20, decimal_places=6)
    hydro_volume = models.DecimalField(max_digits=20, decimal_places=6)
    atomic_volume = models.DecimalField(max_digits=20, decimal_places=6)
    renewable_volume = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:

        indexes = [
            models.Index(fields=['observation_date']),
            models.Index(fields=['price_zone_code']),      
        ]  

        constraints = [ 
            models.UniqueConstraint(fields=['observation_date', 'price_zone_code'], name="unique-price-per-date-zone") 
        ]