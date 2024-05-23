from django.db import models

DECIMAL_DEFAULT_KWARGS = {"decimal_places": 2, "max_digits": 8}


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
