# Django language import:
from django.utils.translation import gettext_lazy as _

# Django Import:
from django.db import models

# Models Import:
from .log_model import Log

# Logger models:
class LogDetails(models.Model):

    class Meta:
        
        # Model name values:
        verbose_name = _('Log detail')
        verbose_name_plural = _('Logs details')

        # Permission values:
        default_permissions = ['read_only', 'read_write']
        permissions = []

    # Corelation witch log model:
    log = models.ForeignKey(Log, on_delete=models.CASCADE)

    # Log details data:
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

    # Model representation:
    def __str__(self) -> str:
        return f'{self.pk} - {self.name}'
