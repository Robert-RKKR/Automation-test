# Django language import:
from django.utils.translation import gettext_lazy as _

# Django Import:
from django.db import models

# Constants:
SEVERITY = (
    (1, 'CRITICAL'),
    (2, 'ERROR'),
    (3, 'WARNING'),
    (4, 'INFO'),
    (5, 'DEBUG'),
)

# Logger models:
class Log(models.Model):

    class Meta:
        
        # Model name values:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')

        # Permission values:
        default_permissions = ['read_only', 'read_write']
        permissions = []

    # Timestamp:
    timestamp = models.DateTimeField(auto_now_add=True)

    # Log data:
    application = models.CharField(max_length=128)
    severity = models.IntegerField(choices=SEVERITY)
    message = models.CharField(max_length=1024)
    task_id = models.CharField(max_length=128, null=True)
    user_message = models.BooleanField(default=False)

    # Models corelations:

    # Model representation:
    def __str__(self) -> str:
        return f'{self.pk} - {self.message}'
