# Models Imports:
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

    def __init__(self, application: str = 'NoName', user_message: bool = False) -> None:

        # Define application name:
        self.application = application
        self.user_message = user_message

    def critical(self, message: str, task_id: str = None, correlated_object: object = None, **kwarg) -> Log:
        """
            Create a new log based on the following data:

                Method attributes:
                -----------------
                message: string
                    Logging message string value.
                task_id: string
                    Celery task ID.
                correlated_object: object
                    Object of device or other model that is supported.
        """
        # Run proccess of log and details log creation:
        log = self._run(CRITICAL, message, task_id, correlated_object, kwarg)

    def error(self, message: str, task_id: str = None, correlated_object: object = None, **kwarg) -> Log:
        """
            Create a new log based on the following data:

                Method attributes:
                -----------------
                message: string
                    Logging message string value.
                task_id: string
                    Celery task ID.
                correlated_object: object
                    Object of device or other model that is supported.
        """
        # Run proccess of log and details log creation:
        log = self._run(ERROR, message, task_id, correlated_object, kwarg)

    def warning(self, message: str, task_id: str = None, correlated_object: object = None, **kwarg) -> Log:
        """
            Create a new log based on the following data:

                Method attributes:
                -----------------
                message: string
                    Logging message string value.
                task_id: string
                    Celery task ID.
                correlated_object: object
                    Object of device or other model that is supported.
        """
        # Run proccess of log and details log creation:
        log = self._run(WARNING, message, task_id, correlated_object, kwarg)

    def info(self, message: str, task_id: str = None, correlated_object: object = None, **kwarg) -> Log:
        """
            Create a new log based on the following data:

                Method attributes:
                -----------------
                message: string
                    Logging message string value.
                task_id: string
                    Celery task ID.
                correlated_object: object
                    Object of device or other model that is supported.
        """
        # Run proccess of log and details log creation:
        log = self._run(INFO, message, task_id, correlated_object, kwarg)

    def debug(self, message: str, task_id: str = None, correlated_object: object = None, **kwarg) -> Log:
        """
            Create a new log based on the following data:

                Method attributes:
                -----------------
                message: string
                    Logging message string value.
                task_id: string
                    Celery task ID.
                correlated_object: object
                    Object of device or other model that is supported.
        """
        # Run proccess of log and details log creation:
        log = self._run(DEBUG, message, task_id, correlated_object, kwarg)

    def _run(self, severity, message, task_id, correlated_object, kwarg):
        """ Run proccess of log and details log creation. """

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

        ### Check if provided data are valid:

        # Check if correlated_object is a object type:
        if isinstance(correlated_object, object):
            
            # Check object type:
            if correlated_object is None:
                pass
            else:
                raise TypeError('Provided object is not supported by log')

        else:
            raise TypeError('Provided correlated object is not object type')

        # Define new log:
        new_log = None

        # Collect all log data:
        log_data = {
            'application': self._check_data_type(self.application, str),
            'user_message': self._check_data_type(self.user_message, bool),
            'severity': severity,
            'message': self._check_data_type(message, str),
            'task_id': self._check_data_type(task_id, str),
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

            # Collect all log details data:
            log_details_data = {
                'log': log,
                'name': self._check_data_type(data, str),
                'value': self._check_data_type(additional_data[data], str),
            }

            try: # Tyr to create a new log details:
                # Create a new log details:
                LogDetails.objects.create(**log_details_data)
            except:
                # If there was a problem during log details creation process, return False:
                return False

    def _check_data_type(self, data, *args):
        """ Check that the given data is correct. """

        # Check all types:
        for data_type in args:
            if isinstance(data, data_type) or data is None:
                return data

        # If the data provided is of an incorrect type, a type error will be raised:
        raise TypeError(f'Provided data "{data}" is not {args} type. Insted is {type(data)} type.')
