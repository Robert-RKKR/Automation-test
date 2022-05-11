# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '2.0'

# Python Import:
import time

# Napalm Import:
import napalm

# Connection Import:
from .connection import Connection

# Device name translation Import:
from .device_name_translation import collect_device_id_from_name
from .device_name_translation import collect_device_name_from_id

# Logger import:
from logger.logger import Logger

# Logger class initiation:
logger = Logger('SSH Napalm connection')


# Main NapCon class:
class NapCon(Connection):
    """
    The NapCon class uses Napalm library, to establish a SSH connection with networks device.

    Methods:
    --------
    send_command:
        Executes commands that do not require privileged mode.
    config_commands:
        Executes commands that require privileged mode.
    """

    def _ssh_connect(self, autodetect: bool = False) -> None:
        """ 
        Connect to device using SSH protocol.
        Returns the type of network device.
        """

        # Check if device is supported before connection attempt:
        if self.supported_device is not None:

            # Performs a specified number of SSH connection attempts to a specified device.
            for connection_attempts in range(1, self.repeat_connection + 1):

                if connection_attempts != self.repeat_connection:
                    time.sleep(1)

                # Log stat of a new SSH connection attempt:
                logger.debug(
                    f'SSH connection to device {self.device_hostname} has been started (Attempt: {connection_attempts}).',
                    self.task_id, self.device_name)

                try: # Try connect to device, using SSH protocol:
                    # Create driver and connect do network device:
                    driver = napalm.get_network_driver(self.self._check_device_type_name())
                    self.connection = driver(
                        hostname=self.device_hostname,
                        username=self.device_username,
                        password=self.device_password,
                        optional_args={
                            'port': self.device_ssh_port},)
                    self.connection.open()
                
                # Handel SSH connection exceptions:
                except napalm.base.exceptions.ConnectionException as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status

                else:
                    # Start session timer:
                    self.connection_timer = time.perf_counter()
                    # Change connection status to True.
                    self.connection_status = True
                    # Log the start of a new connection:
                    logger.info(
                        f'SSH connection to device {self.device_hostname} has been established (Attempt: {connection_attempts}).',
                        self.task_id, self.device_name)

    def _check_device_type_name(self):
        """ Change device type ID to proper Netmiko device name. """

        return collect_device_name_from_id(self.device_type, netmiko=True)
