# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '1.1'

# Python Import:
import time

# Netmiko Import:
from paramiko import ssh_exception
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_exception import  AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

# Model Import:
from inventory.models.device import DeviceType
from inventory.models.device import Device

# Logger import:
from logger.logger import Logger


class NetCon:

    # Logger class initiation:
    logger = Logger('SSH Netconf connection')

    def __init__(self, device: Device, task_id: str = None, repeat_connection: int = 3) -> None:
        """
        The NetCon class uses netmiko library, to establish a SSH connection with networks device.
        
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
        enable_commands: (command)
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

        # Verify if the specified taks_id variable is a string:
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

        # Session timer declaration:
        self.session_timer = None

        # Device unsupported declaration:
        self.unsupported = None

        # Depending on the type of network device, connect to the device using SSH protocol.
        # Or specify the type of device first (If device type is autodetect).

        # Check if the device type must be detected automatically:
        if self.device_type == 'autodetect':

            # Connect to device to check device type, using SSH protocol:
            self.update_device_type()
            
        # Connect to device, using SSH protocol:
        self.connection = self._ssh_connect()

    def _ssh_connect(self, autodetect: bool = False) -> str:
        """ 
        Connect to device using SSH protocol.
        Returns the type of network device.
        
        """

        # Performs a specified number of SSH connection attempts to a specified device.
        for i in range(1, self.repeat_connection + 1):
        
            try: # Try connect to device, using SSH protocol:

                # Log start of SSH connection:
                NetCon.logger.debug(
                    f'SSH connection to device {self.hostname} has been started (Attempt: {i}).',
                    self.task_id, self.device
                )
            
                # Check if the device type must be detected automatically:
                if autodetect:

                    # Connect to device to check device type, using SSH protocol:
                    connection = SSHDetect(**{
                        'device_type': 'autodetect',
                        'host': self.hostname,
                        'username': self.username,
                        'password': self.password,
                        'port': self.ssh_port,
                    })
                
                else:

                    # Connect to device, using SSH protocol:
                    connection = ConnectHandler(**{
                        'device_type': self.device_type,
                        'host': self.hostname,
                        'username': self.username,
                        'password': self.password,
                        'port': self.ssh_port,
                        'secret': self.password,
                    })

            # Handel SSH connection exceptions:
            except AuthenticationException as error:
                NetCon.logger.error(error, self.task_id, self.device)
                # Change connection status to False:
                self.status = False
                # Wait 1 second i case of connection failure:
                if self.repeat_connection == i:
                    # Return connection starus:
                    return self.status
                else:
                    time.sleep(1)

            except NetMikoTimeoutException as error:
                NetCon.logger.error(error, self.task_id, self.device)
                # Change connection status to False:
                self.status = False
                # Wait 1 second i case of connection failure:
                if self.repeat_connection == i:
                    # Return connection starus:
                    return self.status
                else:
                    time.sleep(1)

            except ssh_exception.SSHException as error:
                NetCon.logger.error(error, self.task_id, self.device)
                # Change connection status to False:
                self.status = False
                # Wait 1 second i case of connection failure:
                if self.repeat_connection == i:
                    # Return connection starus:
                    return self.status
                else:
                    time.sleep(1)

            else:

                # Start session timer:
                self.session_timer = time.perf_counter()

                # Log end of SSH connection
                NetCon.logger.info(
                    f'SSH connection to device {self.hostname} has been established (Attempt: {i}).',
                    self.task_id, self.device
                )
                # Change connection status to True.
                self.status = True

                if autodetect:
                
                    # Collect information about device type:
                    return connection.autodetect()

                else:

                    # Return connection:
                    return connection

    def __repr__(self) -> str:
        """ Connection class representation is IP address and port number of Https server. """
        return self.device.hostname

    def close(self):
        """ End of SSH connection """

        # Close SSH connection:
        self.connection.disconnect()
        # End session timer:
        finish_time = time.perf_counter()
        self.session_timer = round(finish_time - self.session_timer, 5)
        # Log close of SSH connection:
        NetCon.logger.info('SSH session ended.', self.task_id, self.device)
        # Log time of SSH session:
        if self.session_timer > 2:
            NetCon.logger.debug(
                f'SSH session was active for {self.session_timer} seconds.',
                self.task_id, self.device
            )
        else:
            NetCon.logger.debug(
                f'SSH session was active for {self.session_timer} second.',
                self.task_id, self.device
            )

    def check_device_type(self) -> str:
        """ Obtain network device type information using SSH protocol. """

        return self._ssh_connect(autodetect=True)

    def update_device_type(self) -> str:
        """ Obtain network device type information using SSH protocol. And update Device type object. """

        # Log begining of network device type checking proccess:
        NetCon.logger.info(
            'Started acquiring information about the type of network device.',
            self.task_id, self.device
        )

        # Connect to device to check device type, using SSH protocol:
        device_type = self._ssh_connect(autodetect=True)

        try: # Collect device type object that match the current criteria:
            device_type_object = DeviceType.objects.get(value=device_type)
        
        except: # If the device type does not match the criteria, it means that the device is not supported:
            NetCon.logger.info(
                f'Device {self.name} currently possess an unsupported system {device_type}.',
                self.task_id, self.device
            )
            # Change unsupported status to True:
            self.unsupported = True
            # Change connection status to False:
            self.status = False
            # Return connection starus:

        else:
            # update current device type name:
            self.device_type = device_type_object.value
            # Log end of SSH connection:
            NetCon.logger.info(
                f'Information about the type of device was collected (Device type is: {self.device_type}).',
                self.task_id, self.device
            )

        # Update current device type object:
        try:
            # Update device object:
            self.device.device_type = device_type_object
            self.device.save()
        
        except: # Return exception if there is a problem during the update of the device type object:
            NetCon.logger.info(
                f'When updating the device type, an exception occurs.',
                self.task_id, self.device
            )

        else:
            # Log end of SSH connection
            NetCon.logger.info('Device object was updated.', self.task_id, self.device)

        return device_type

    def _connection_status(self) -> bool:
        """ Check the connection status and try to re-connect if necessary. """

        # Check connection status:
        if self.status is False:
            # Try to reconnect SSH connection:
            if self._ssh_connect() is False:
                # Log failed confection status:
                NetCon.logger.warning(
                    f'Command/s could not be executed because SSH connection was interrupted.',
                    self.task_id, self.device
                )
                # Return connection starus:
                return False
        else:
            return True

    def _command_execution(self, command: str, expect_string: str = False):
        """ Xxx. """

        # Log start of command execution: 
        NetCon.logger.debug(
            f'Sending of a new CLI command "{command}" has been started.',
            self.task_id, self.device
        )

        try:
            if expect_string is False:
                return_data = self.connection.send_command(
                    command_string=command
                )
            else:
                return_data = self.connection.send_command(
                    command_string=command,
                    expect_string=expect_string
                )

        except UnboundLocalError as error:
            NetCon.logger.error(error, self.task_id, self.device)
            # Change connection status to False:
            self.status = False
            # Return connection starus:
            return False

        except OSError as error:
            NetCon.logger.error(error, self.task_id, self.device)
            # Change connection status to False:
            self.status = False
            # Return connection starus:
            return False

        else:
            # Log end of command execution:
            NetCon.logger.info(
                f'The CLI command "{command}" has been sent.',
                self.task_id, self.device
            )
            # Return command output:
            return return_data

    def enable_commands(self, commands: str or list, expect_string: str = False) -> str or list:
        """
        Retrieves a string or list containing network CLI commands, and sends them to a network device using SSH protocol.
        ! Usable only with enable levels commend/s.
        
        Parameters:
        -----------------
        commands: String
            Provided device object, to establish a SSH connection.
        commands: List
            Provided device object, to establish a SSH connection.
        expect_string: String
            Specifies the Celery task ID value, that will be added to logs messages.

        Return:
        --------
        String containing command/s output.
        """

        if isinstance(commands, str) or isinstance(commands, list):
            pass
        else:
            # Raise exception:
            raise TypeError('The provided command/s variable must be a string or list.')

        # Check connection status:
        if self._connection_status():

            # Start clock count:
            start_time = time.perf_counter()

            # Collect data from device:
            return_data = None

            if isinstance(commands, str):
                return_data = self._command_execution(commands, expect_string)

            elif isinstance(commands, list):
                # Create temporary dictionary:
                temporary_data = {}
                # Run command execution one by one:
                for command in commands:
                    if isinstance(command, str):
                        temporary_data[command] = return_data = self._command_execution(command)
                    elif isinstance(command, dict):
                        self._command_execution(
                            command['command'],
                            command['expect_string']
                        )
                    else:
                        # Raise exception:
                        raise TypeError('Xxxxxxx.')
                # Add temporary dictionary to return data:
                return_data = temporary_data

            # Finish clock count & method execution time:
            finish_time = time.perf_counter()
            self.execution_time = round(finish_time - start_time, 5)

            # Log time of command/s execution:
            if self.execution_time > 2:
                NetCon.logger.debug(
                    f'Execution of "{commands}" command/s taken {self.execution_time} seconds.',
                    self.task_id, self.device
                )
            else:
                NetCon.logger.debug(
                    f'Execution of "{commands}" command/s taken {self.execution_time} second.',
                    self.task_id, self.device
                )
            
            # Return data:
            return return_data

    def config_commands(self, command) -> str:
        """ 
        Takes list of strings or string (Networks commands), and send to network device using SSH protocol.
        Usable only with configuration terminal levels commends.
        """

        # Check connection status:
        if self.status is False:
            return False
        else:

            # Start clock count:
            start_time = time.perf_counter()

            # Collect data from device:
            return_data = None

            # Try to sent command into network device:
            try:
                NetCon.logger.debug(
                    f'Sending of a new CLI command "{command}" has started.',
                    self.task_id, self.device
                )
                return_data = self.connection.send_config_set(command)
                NetCon.logger.info(
                    f'The CLI command "{command}" has been sent.',
                    self.task_id, self.device
                )
            except UnboundLocalError as error:
                NetCon.logger.error(error, self.task_id, self.device)
                return error

            # Finish clock count & method execution time:
            finish_time = time.perf_counter()
            self.execution_time = round(finish_time - start_time, 5)

            # Log time of command execution:
            if self.execution_time > 2:
                NetCon.logger.debug(
                    f'Execution of "{command}" command taken {self.execution_time} seconds.',
                    self.task_id, self.device
                )
            else:
                NetCon.logger.debug(
                    f'Execution of "{command}" command taken {self.execution_time} second.',
                    self.task_id, self.device
                )

            # Return data:
            return return_data
