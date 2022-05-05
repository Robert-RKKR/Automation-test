# Django Import:
from django.db import models

# Base Model Import:
from main.basemodel import BaseMainModel


# Model code:
class Credential(BaseMainModel):
    """ 
        The Credential specifies the login information (Login, password)
        needed in the login process when connecting to network devices.
    """

    # Main model values:
    username = models.CharField(
        max_length=64,
        error_messages={
            'null': 'Username field is mandatory.',
            'blank': 'Username field is mandatory.',
            'invalid': 'Enter the correct username value.',
        },
    )
    password = models.CharField(max_length=64, null=True, blank=True)
