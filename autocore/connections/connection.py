# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '1.0'

# Model Import:
from inventory.models.device import Device


class Connection:
    """
    Basic connection class.
    
    Attributes:
    -----------------
    device_name:
        Xxx.
    device_hostname:
        Xxx.
    device_ssh_port:
        Xxx.
    device_https_port:
        Xxx.
    device_certificate:
        Xxx.
    device_username:
        Xxx.
    device_password:
        Xxx.
    device_type:
        Xxx.
    connection_status:
        Xxx.
    execution_time:
        Xxx.
    connection_timer:
        Xxx.
    supported_device:
        Xxx.
    repeat_connection:
        Xxx.
    """

    def __init__(self, device: Device, task_id: str = None, repeat_connection: int = 3) -> None:
        """
        Parameters:
        -----------------
        device: Device object
            Provided device object, to establish network connection.
        task_id: String
            Specifies the Celery task ID value, that will be added to logs messages.
        repeat_connection: Intiger
            Specifies how many times the network connection will be retried.
        """

        # Verify if the specified device variable is a valid Device object:
        if isinstance(device, Device):
            try:
                # Collect basic device data:
                self.device = device
                self.device_name = device.name
                self.device_hostname = device.hostname
                self.device_ssh_port = device.ssh_port
                self.device_certificate = device.https_port
                self.device_type = device.device_type

                # Collect user data:
                if device.credential is None:
                    # Use default user data:
                    self.device_username = 'admin'
                    self.device_password = 'password'
                else: # Collect username and password from credential Model:
                    self.device_username = device.credential.username
                    self.device_password = device.credential.password
            except:
                self._raise_exception(
                    'Provided device object is not compatible with connection class.')

        else:
            # Change connection status to False:
            self.connection_status = False
            # Raise exception:
            raise TypeError('The provided device variable must be a valid object of the Device class.')

        # Verify if the specified taks_id variable is a string:
        if task_id is None or isinstance(task_id, str):
            # Celery task ID declaration:
            self.task_id = task_id
        else:
            # Change connection status to False:
            self.connection_status = False
            # Raise exception:
            raise TypeError('The provided task ID variable must be a string.')

        # Verify if the specified repeat_connection variable is a string:
        if repeat_connection is None or isinstance(repeat_connection, int):
            # Celery task ID declaration:
            self.repeat_connection = repeat_connection
        else:
            # Change connection status to False:
            self.connection_status = False
            # Raise exception:
            raise TypeError('The provided repeat connection variable must be a intiger.')

        # Connection status declaration:
        self.connection_status = None

        # Execution timer declaration:
        self.execution_time = None

        # Session timer declaration:
        self.connection_timer = None

        # Device supported declaration:
        if self.device_type == 0:
            self.supported_device = None
        elif self.device_type == 99:
            self.supported_device = False
        else:
            self.supported_device = True

    def __repr__(self) -> str:
        """ Class representation. """
        return f'<Class connection ({self.device_name}/{self.device_hostname})>'

    def _raise_exception(self, exception):
        """ Xxx. """

        # Change connection status tu False:
        self.connection_status = False
        # Raise exception:
        raise TypeError(exception)

    def _log_error(self, logger, error):
        """ Xxx. """

        # Log error:
        logger.error(error, self.task_id, self.device_name)
        # Change connection status to False:
        self.connection_status = False
