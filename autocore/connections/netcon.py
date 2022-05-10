# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '2.1'

# Netmiko Import:
from paramiko import ssh_exception
from netmiko import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_exception import  AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException

# Connection Import:
from .connection import Connection

# Device name translation Import:
from .device_name_translation import collect_device_id_from_name
from .device_name_translation import collect_device_name_from_id

# Logger import:
from logger.logger import Logger

# Logger class initiation:
logger = Logger('SSH Netconf connection')


# Main NetCon class:
class NetCon(Connection):
    """
    The NetCon class uses netmiko library, to establish a SSH connection with networks device.

    Methods:
    --------
    update_device_type:
        Collect device type via SSH protocol and updates device type attributes of device object.
    close_connection:
        Close SSH connection.
    enabled_commands:
        Executes commands that do not require privileged mode.
    configuration_commands:
        Executes commands that require privileged mode.
    """

    def _ssh_connect(self, autodetect: bool = False) -> str:
        """ 
        Connect to device using SSH protocol.
        Returns the type of network device.
        """

        # Check if device is supported before connection attempt:
        if self.supported_device is False:

            # Log unsupported device type:
            self._log_error(logger, f'Device {self.device_hostname} is not supported')
            return False

        elif self.supported_device or autodetect:

            # Performs a specified number of SSH connection attempts to a specified device.
            for connection_attempts in range(1, self.repeat_connection + 1):

                if connection_attempts != self.repeat_connection:
                    self._sleep()

                # Log stat of a new SSH connection attempt:
                logger.debug(
                    f'SSH connection to device {self.device_hostname} has been started (Attempt: {connection_attempts}).',
                    self.task_id, self.device_name)

                try: # Try connect to device, using SSH protocol:
                    # Check if the device type must be detected automatically:
                    if autodetect:
                        # Connect to device to check device type, using SSH protocol:
                        self.connection = SSHDetect(**{
                            'device_type': 'autodetect',
                            'host': self.device_hostname,
                            'port': self.device_ssh_port,
                            'username': self.device_username,
                            'password': self.device_password})
                    else:
                        # Connect to device, using SSH protocol:
                        self.connection = ConnectHandler(**{
                            'device_type': self._check_device_type_name(),
                            'host': self.device_hostname,
                            'port': self.device_ssh_port,
                            'username': self.device_username,
                            'password': self.device_password})

                # Handel SSH connection exceptions:
                except AuthenticationException as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status
                except NetMikoTimeoutException as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status
                except ssh_exception.SSHException as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status
                except OSError as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status
                except TypeError as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status
                except ValueError as error:
                    self._log_error(logger, error)
                    # Return connection starus:
                    return self.connection_status

                else:
                    # Change connection status to True.
                    self.connection_status = True
                    # Log the start of a new connection:
                    logger.info(
                        f'SSH connection to device {self.device_hostname} has been established (Attempt: {connection_attempts}).',
                        self.task_id, self.device_name)

                    if autodetect:    
                        # Collect information about device type:
                        return self.connection.autodetect()
                    else: # Return connection:
                        return self.connection

    def _check_device_type_name(self):
        """ Change device type ID to proper Netmiko device name. """

        return collect_device_name_from_id(self.device_type, netmiko=True)

    def _enabled_command_execution(self, command: str, expect_string: str = False) -> str:
        """ Enabled CLI command execution. """

        # Log start of command execution: 
        logger.debug(
            f'Sending of a new enabled CLI command "{command}" has been started.',
            self.task_id, self.device_name)

        try:
            if expect_string is False:
                return_data = self.connection.send_command(
                    command_string=command)
            else:
                return_data = self.connection.send_command(
                    command_string=command,
                    expect_string=expect_string)

        except UnboundLocalError as error:
            self._log_error(logger, error)
            # Return connection starus:
            return self.connection_status
        except OSError as error:
            self._log_error(logger, error)
            # Return connection starus:
            return self.connection_status
        except TypeError as error:
            self._log_error(logger, error)
            # Return connection starus:
            return self.connection_status

        else:
            # Log end of command execution:
            logger.info(
                f'The enabled CLI command "{command}" has been sent.',
                self.task_id, self.device_name)
            # Return command output:
            return return_data

    def _config_command_execution(self, command: str) -> str:
        """ Configuration CLI command execution. """

        # Log start of command execution: 
        logger.debug(
            f'Sending of a new configuration CLI command "{command}" has been started.',
            self.task_id, self.device_name)

        try:
            return_data = self.connection.send_config_set(command)

        except UnboundLocalError as error:
            self._log_error(logger, error)
            # Return connection starus:
            return self.connection_status
        except OSError as error:
            self._log_error(logger, error)
            # Return connection starus:
            return self.connection_status
        except TypeError as error:
            self._log_error(logger, error)
            # Return connection starus:
            return self.connection_status

        else:
            # Log end of command execution:
            logger.info(
                f'The configuration CLI command "{command}" has been sent.',
                self.task_id, self.device_name)
            # Return command output:
            return return_data

    def open_connection(self):
        """ Open a new SSH connection """

        # Check if device need autodetect process:
        if self.supported_device is None:
            # Update device type based on information collected via SSH protocol:
            self.update_device_type()
            # Connect to network device:
            self._ssh_connect()
        # Check connection status:
        elif self.connection_status is not True:
            self._ssh_connect()

        # Start connection timer if connected successfully:
        if self.connection_status:
            # Start session timer:
            self.connection_timer = self._start_connection_timer()
    
    def close_connection(self):
        """ End of SSH connection """

        # Check connection status:
        if self.connection_status:
            # Close SSH connection:
            self.connection.disconnect()
            # Log close of SSH connection:
            logger.info('SSH session ended.', self.task_id, self.device_name)
            # End session timer:
            self._end_connection_timer(logger)

    def update_device_type(self):
        """ Obtain network device type information using SSH protocol. And update Device type object. """

        # Log begining of network device type checking proccess:
        logger.info(
            'Started acquiring information about the type of network device.',
            self.task_id, self.device_name)

        # Connect to device to check device type, using SSH protocol:
        discovered_device_type = self._ssh_connect(autodetect=True)

        # Collect device type ID:
        device_name_id = collect_device_id_from_name(discovered_device_type, netmiko=True)

        if device_name_id:
            try: # Update current device object:
                # Update device object:
                self.device.device_type = device_name_id
                self.device.save()         
            except: # Return exception if there is a problem during the update of the device type object:
                logger.info(
                    f'When updating the device type, an exception occurs.',
                    self.task_id, self.device_name)
                # Return collected device type name:
                return discovered_device_type
            else:
                # Log end of SSH connection
                logger.info(
                    'Device object has been updated.',
                    self.task_id, self.device_name)
                # Update device type attribute:
                self.device_type = device_name_id
                # Return collected device type name:
                return discovered_device_type
        
        else:
            # Inform that current device type is not supported:
            self._log_error(logger, f'Device {self.device_hostname} is currently not supported.')
            # Return collected device type name:
            return discovered_device_type

    def enabled_commands(self, commands: str or list, expect_string: str = False, api: bool = False) -> str or list:
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
        api: bool
            If True, method will return output in dictionary format (Using regex).

        Return:
        --------
        String containing command/s output.
        """

        # Check if provided command variable is valid string or list:
        if isinstance(commands, str) or isinstance(commands, list):
            pass
        else:
            # Raise exception:
            raise TypeError('The provided command/s variable must be a string or list.')
            
        # Check if provided expect string variable is valid string:
        if isinstance(expect_string, str) or expect_string is False:
            pass
        else:
            # Raise exception:
            raise TypeError('The provided expect string variable must be a string.')

        # Check connection status:
        if self.connection_status:

            # Start clock count:
            start_time = self._start_execution_timer()

            # Collect data from device:
            return_data = None

            if isinstance(commands, str):
                return_data = self._enabled_command_execution(commands, expect_string)

            elif isinstance(commands, list):
                # Create temporary dictionary:
                temporary_data = {}
                # Run command execution one by one:
                for command in commands:
                    if isinstance(command, str):
                        temporary_data[command] = self._enabled_command_execution(command)
                    elif isinstance(command, list):
                        return_data = self._enabled_command_execution(
                            command[0], command[1])
                    else:
                        # Raise exception:
                        raise TypeError('Wrong data type.')
                # Add temporary dictionary to return data:
                return_data = temporary_data

            # Finish clock count & method execution time:
            self._end_execution_timer(start_time, logger, commands)
            
            # Return data:
            if api:
                pass
            else:
                return return_data

        else:
            # Inform that the command cannot be sent:
            self._log_error(
                logger, 'Command/s could not be executed because SSH connection was interrupted.')

    def configuration_commands(self, commands: str or list) -> str:
        """
        Retrieves a string or list containing network CLI commands, and sends them to a network device using SSH protocol.
        ! Usable only with configuration terminal levels commends.
        
        Parameters:
        -----------------
        commands: String
            Provided device object, to establish a SSH connection.
        commands: List
            Provided device object, to establish a SSH connection.

        Return:
        --------
        String containing command/s output.
        """

        # Check if provided command variable is valid string or list:
        if isinstance(commands, str) or isinstance(commands, list):
            pass
        else:
            # Raise exception:
            raise TypeError('The provided command/s variable must be a string or list.')

        # Check connection status:
        if self.connection_status:

            # Start clock count:
            start_time = self._start_execution_timer()

            # Collect data from device:
            return_data = self._config_command_execution(commands)

            # Finish clock count & method execution time:
            self._end_execution_timer(start_time, logger, commands)

            # Return data:
            return return_data

        else:
            # Inform that the command cannot be sent:
            self._log_error(
                logger, 'Command/s could not be executed because SSH connection was interrupted.')
