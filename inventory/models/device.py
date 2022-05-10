# Django Import:
from django.db import models

# Applications Import:
from autocore.connections.device_name_translation import DEVICE_TYPE
from .icons import ICONS

# Other models Import:
from .credential import Credential

# Base Model Import:
from main.basemodel import BaseMainModel
from main.basemodel import BaseSubModel


# Model code:
class Device(BaseMainModel):
    """ 
        Devices is the main component of the AutoCli application,
        it contains basic network Information about devices that
        are not collected directly from the devices themselves.
    """

    # Device status:
    ssh_status = models.BooleanField(default=False)
    https_status = models.BooleanField(default=False)

    # Main model values:
    hostname = models.CharField(
        max_length=32,
        blank=False,
        unique=True,
        error_messages={
            'null': 'IP / DNS name field is mandatory.',
            'blank': 'IP / DNS name field is mandatory.',
            'unique': 'Device with this hostname already exists.',
            'invalid': 'Enter a valid IP address or DNS resolvable hostname. It must contain 4 to 32 digits, letters and special characters -, _, . or spaces.',
        },
    )
    device_type = models.IntegerField(choices=DEVICE_TYPE, default=0)
    ico = models.IntegerField(choices=ICONS, default=0)
    ssh_port = models.IntegerField(default=22)
    https_port = models.IntegerField(default=443)

    # Security and credentials:
    credential = models.ForeignKey(Credential, on_delete=models.PROTECT, null=True, blank=True)
    secret = models.CharField(max_length=64, null=True, blank=True)
    token = models.CharField(max_length=128, null=True, blank=True)
    certificate = models.BooleanField(default=False)


class DeviceData(BaseSubModel):

    # Corelation witch device model:
    device = models.OneToOneField(Device, on_delete=models.CASCADE)

    # Show version output:
    version = models.CharField(max_length=64, blank=True, null=True)
    hostname = models.CharField(max_length=64, blank=True, null=True)
    uptime = models.CharField(max_length=64, blank=True, null=True)
    reload_reason = models.CharField(max_length=64, blank=True, null=True)
    running_image = models.CharField(max_length=64, blank=True, null=True)
    config_register = models.CharField(max_length=64, blank=True, null=True)
    hardware_list = models.JSONField(blank=True, null=True)
    serial_list = models.JSONField(blank=True, null=True)
    mac_list = models.JSONField(blank=True, null=True)

    # Model representation:
    def __str__(self) -> str:
        return f"DeviceData({self.pk}: device({self.device}))"


class DeviceInterface(BaseSubModel):

    # Corelation witch device model and unique:
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)

    # # Show interfaces status output:
    # name = models.CharField(max_length=64, blank=True, null=True)
    # status = models.CharField(max_length=64, blank=True, null=True)
    # vlan = models.CharField(max_length=64, blank=True, null=True)
    # type = models.CharField(max_length=64, blank=True, null=True)

    # Show interfaces output:
    link_status = models.CharField(max_length=64, blank=True, null=True)
    protocol_status = models.CharField(max_length=64, blank=True, null=True)
    hardware_type = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    bia = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    ip_address = models.CharField(max_length=64, blank=True, null=True)
    mtu = models.CharField(max_length=64, blank=True, null=True)
    duplex = models.CharField(max_length=64, blank=True, null=True)
    speed = models.CharField(max_length=64, blank=True, null=True)
    media_type = models.CharField(max_length=64, blank=True, null=True)
    bandwidth = models.CharField(max_length=64, blank=True, null=True)
    delay = models.CharField(max_length=64, blank=True, null=True)
    encapsulation = models.CharField(max_length=64, blank=True, null=True)
    last_input = models.CharField(max_length=64, blank=True, null=True)
    last_output = models.CharField(max_length=64, blank=True, null=True)
    last_output_hang = models.CharField(max_length=64, blank=True, null=True)
    queue_strategy = models.CharField(max_length=64, blank=True, null=True)
    input_rate = models.CharField(max_length=64, blank=True, null=True)
    output_rate = models.CharField(max_length=64, blank=True, null=True)
    input_packets = models.CharField(max_length=64, blank=True, null=True)
    output_packets = models.CharField(max_length=64, blank=True, null=True)
    input_errors = models.CharField(max_length=64, blank=True, null=True)
    crc = models.CharField(max_length=64, blank=True, null=True)
    abort = models.CharField(max_length=64, blank=True, null=True)
    output_errors = models.CharField(max_length=64, blank=True, null=True)


    # Model representation:
    def __str__(self) -> str:
        return f"{self.pk}: {self.name}: device({self.device})"

    class Meta:
        unique_together = [['device', 'name']]


class DeviceRawData(BaseSubModel):

    # Corelation witch device model:
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    # Command raw data:
    command_name = models.CharField(max_length=64)
    command_data = models.TextField(null=True, blank=True)

    # Model representation:
    def __str__(self) -> str:
        return f"DeviceRawData({self.pk}: device({self.device}), '{self.command_name}')"

    class Meta:
        unique_together = [['device', 'command_name']]

