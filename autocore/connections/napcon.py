# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '2.1'

# Python Import:
import time

# Netmiko Import:
from paramiko import ssh_exception
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_exception import  AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException

# Model Import:
from inventory.models.device import Device

# Logger import:
from logger.logger import Logger

# Device type ID to name translation:
DEVICE_TYPE = {
    1: 'cisco_ios',
    2: 'cisco_xe',
    3: 'cisco_xr',
    4: 'cisco_nxos',
    5: 'cisco_asa',
}
