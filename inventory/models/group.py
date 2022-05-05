# Django Import:
from django.db import models

# Other models Import:
from .device import Device

# Base Model Import:
from main.basemodel import BaseMainModel


# Model code:
class Group(BaseMainModel):
    """ Groups allow you to group network devices. """

    # Relationships with other models:
    devices = models.ManyToManyField(Device)
