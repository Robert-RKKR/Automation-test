# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '1.1'

# Python Import:
import time

# Napalm Import:
from napalm import get_network_driver

# Model Import:
from inventory.models.device import DeviceType
from inventory.models.device import Device

# Logger import:
from logger.logger import Logger

class NapCon:

    # Logger class initiation:
    logger = Logger('SSH Napalm connection')

    def __init__(self, device: Device, task_id: str = None, repeat_connection: int = 3) -> None:
        """
        The NapCon class uses Napalm library, to establish a SSH connection with networks device.
        
        Class attributes:
        -----------------
        device: Device object
            Provided device object, to establish a SSH connection.
        task_id: String
            Specifies the Celery task ID value, that will be added to logs messages.
        repeat_connection: Intiger
            Specifies how many times the SSH connection will be retried.
        
        Methods:
        --------
        send_command: (command)
            Executes commands that do not require privileged mode.
        config_commands: (command)
            Executes commands that require privileged mode.
        """

        # Verify if the specified device variable is a valid Device object:
        if isinstance(device, Device):
            # Device declaration:
            self.name = device.name
            self.hostname = device.hostname
            self.ssh_port = device.ssh_port
            self.certificate = device.certificate
            self.device = device
        else:
            # Change connection status to False:
            self.status = False
            # Raise exception:
            raise TypeError('The provided device variable must be a valid object of the Device class.')

        # Verify if the specified taks id variable is a string:
        if task_id is None or isinstance(task_id, str):
            # Celery task ID declaration:
            self.task_id = task_id
        else:
            # Change connection status to False:
            self.status = False
            # Raise exception:
            raise TypeError('The provided task ID variable must be a string.')

        # Verify if the specified repeat_connection variable is a string:
        if repeat_connection is None or isinstance(repeat_connection, int):
            # Celery task ID declaration:
            self.repeat_connection = repeat_connection
        else:
            # Change connection status to False:
            self.status = False
            # Raise exception:
            raise TypeError('The provided repeat connection variable must be a intiger.')

        # Specify the device type name:
        if self.device.device_type is None:
            # If the device type is not specified, treat the device as automatically detected:
            self.device_type = 'autodetect'
        else: # If a device type is given, get the name of the device type:
            self.device_type = self.device.device_type.value

        # Collect user data:
        if self.device.credential is None:
            # Use default user data:
            self.username = 'admin'
            self.password = 'password'
        else: # Collect username and password from credential Model:
            self.username = self.device.credential.username
            self.password = self.device.credential.password

        # Connection status declaration:
        self.status = None

        # Execution timer declaration:
        self.execution_time = None

        # Device unsupported declaration:
        self.unsupported = None









from napalm import get_network_driver

driver = get_network_driver('ios')
device = driver(
    hostname='sandbox-iosxe-latest-1.cisco.com',
    username='developer',
    password='C1sco12345',
    optional_args={'port': 22},
)
device.open()
device.load_merge_candidate(filename='autocore/comands.conf')
#device.load_merge_candidate(config='hostname test\ninterface Ethernet2\ndescription bla')
print(device.compare_config())

while(True):
    output = input('Are you happy? y/n: ')
    if output == 'y':
        device.commit_config()
        print('Changes accepted!')
        break
    elif output == 'n':
        device.discard_config()
        print('Changes discarded!')
        break
