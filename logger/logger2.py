# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '1.0'

# Model Import:
from .models.log_details_model import LogDetails
from .models.log_model import Log

# Severity constants declaration:
DEBUG = 5
INFO = 4
WARNING = 3
ERROR = 2
CRITICAL = 1

# Main Logger class:
class Logger:
    """
    Logger class.
    
    Attributes:
    -----------------
    application:
        Xxx.
    user_message:
        Xxx.

    Methods:
    --------
    critical:
        Xxx.
    error:
        Xxx.
    warning:
        Xxx.
    info:
        Xxx.
    debug:
        Xxx.
    """

    def __init__(self, application: str = 'NoName', user_message: bool = False) -> None:
        """ Log application acclivity. """

        # Verify if the application variable is a valid sting:
        if isinstance(application, str):
            self.application = application
        else:
            raise TypeError('The provided application variable must be string.')
        
        # Verify if the user message variable is a valid boolean:
        if isinstance(user_message, bool):
            self.user_message = user_message
        else:
            raise TypeError('The provided user message variable must be boolean.')

    def critical(self, message: str, task_id: str = None, correlated_object: str = None, **kwarg) -> Log:
        """
        Create a new log based on the following data:

        Parameters:
        -----------------
        message: string
            Logging message string value.
        task_id: string
            Celery task ID.
        correlated_object: object
            Object of device or other model that is supported.
        """

        # Run proccess of log and details log creation:
        return self._run(CRITICAL, message, task_id, correlated_object, kwarg)

    def error(self, message: str, task_id: str = None, correlated_object: str = None, **kwarg) -> Log:
        """
        Create a new log based on the following data:

        Parameters:
        -----------------
        message: string
            Logging message string value.
        task_id: string
            Celery task ID.
        correlated_object: object
            Object of device or other model that is supported.
        """
        
        # Run proccess of log and details log creation:
        return self._run(ERROR, message, task_id, correlated_object, kwarg)

    def warning(self, message: str, task_id: str = None, correlated_object: str = None, **kwarg) -> Log:
        """
        Create a new log based on the following data:

        Parameters:
        -----------------
        message: string
            Logging message string value.
        task_id: string
            Celery task ID.
        correlated_object: object
            Object of device or other model that is supported.
        """

        # Run proccess of log and details log creation:
        return self._run(WARNING, message, task_id, correlated_object, kwarg)

    def info(self, message: str, task_id: str = None, correlated_object: str = None, **kwarg) -> Log:
        """
        Create a new log based on the following data:

        Parameters:
        -----------------
        message: string
            Logging message string value.
        task_id: string
            Celery task ID.
        correlated_object: object
            Object of device or other model that is supported.
        """

        # Run proccess of log and details log creation:
        return self._run(INFO, message, task_id, correlated_object, kwarg)

    def debug(self, message: str, task_id: str = None, correlated_object: str = None, **kwarg) -> Log:
        """
        Create a new log based on the following data:

        Parameters:
        -----------------
        message: string
            Logging message string value.
        task_id: string
            Celery task ID.
        correlated_object: object
            Object of device or other model that is supported.
        """

        # Run proccess of log and details log creation:
        return self._run(DEBUG, message, task_id, correlated_object, kwarg)

    def _run(self, severity, message, task_id, correlated_object, kwarg):
        """ Run proccess of log and details log creation. """

        # Check provided data:
        if isinstance(message, str) is False:
            raise TypeError('The provided message variable must be string.')
        if task_id(message, str) is False:
            raise TypeError('The provided task id variable must be string.')
        if isinstance(correlated_object, str) is False:
            raise TypeError('The provided correlated object variable must be string.')

        # Create new log based on provided data:
        log = self._create_log(severity, message, task_id, correlated_object)

        # Check if additional data was provided:
        if kwarg is not None:
            # If additional data was provided, create log details object/s based of provided data:
            self._create_log_details_objects(kwarg, log)

        # return log:
        return log

    def _create_log(self, severity, message, task_id, correlated_object):
        """ Create new log in Database """

        # Define new log:
        new_log = None

        # Collect all log data:
        log_data = {
            'correlated_object': correlated_object,
            'user_message': self.user_message,
            'application': self.application,
            'severity': severity,
            'message': message,
            'task_id': task_id,
        }

        try: # Tyr to create a new log:
            # Create a new log:
            new_log = Log.objects.create(**log_data)
        except:
            # If there was a problem during log creation process, return False:
            return False

        # Return created log object:
        return new_log

    def _create_log_details_objects(self, additional_data, log):
        """ Create new log details in Database """

        for data in additional_data:

            # Check provided data:
            if isinstance(data, str):
                name = data
            else:
                raise TypeError('The provided name variable must be string.')
            if isinstance(data, str):
                value = additional_data[data]
            else:
                raise TypeError('The provided value variable must be string.')

            # Collect all log details data:
            log_details_data = {
                'log': log,
                'name': name,
                'value': value,
            }

            try: # Tyr to create a new log details:
                # Create a new log details:
                LogDetails.objects.create(**log_details_data)
            except:
                # If there was a problem during log details creation process, return False:
                return False
