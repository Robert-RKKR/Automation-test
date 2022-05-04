# Document descryption:
__author__ = 'Robert Tadeusz Kucharski'
__version__ = '1.0'

# Python Import:
import requests
import xmltodict
import json
import time

# Model Import:
from inventory.models.device import Device

# Logger import:
from logger.logger import Logger


class ApiCon:
    
    # Logger class initiation:
    logger = Logger('API connection')

    def __init__(self, device: Device, task_id: str = None, headers: dict = None) -> None:
        """
        The API connection class uses requests library, to connect with network device using HTTPS protocol.
            
        Class attributes:
        -----------------
        device: Device object
            Provided device object, to establish a HTTPS connection.
        task_id: String
            Specifies the Celery task ID value, that will be added to logs messages (Optional).
        headers: dict
            Additional header information (Optional).
        
        Methods:
        --------
        get, post, put, delete.

        Return:
        -------
        None
        """

        # Verify if the specified device variable is a valid Device object:
        if isinstance(device, Device):
            # Device declaration:
            self.hostname = device.hostname
            self.https_port = device.ssh_port
            self.certificate = device.certificate
            self.token = device.token
            self.device = device
        else:
            # Change connection status to False:
            self.status = False
            # Rais exception:
            raise TypeError('The provided device variable must be a valid object of the Device class.')

        # Verify if the specified headers variable is a dictionary:
        if headers is None or isinstance(headers, dict):
            # Headers declaration:
            self.headers = headers
        else:
            # Change connection status to False:
            self.status = False
            # Rais exception:
            raise TypeError('The provided headers variable must be a dictionary.')

        # Verify if the specified taks_id variable is a string:
        if task_id is None or isinstance(task_id, str):
            # Celery task ID declaration:
            self.task_id = task_id
        else:
            # Change connection status to False:
            self.status = False
            # Rais exception:
            raise TypeError('The provided task ID variable must be a string.')

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
        self.xml_status = None
        self.json_status = None
        self.response_code = None

        # Execution timer declaration:
        self.execution_time = None

    def __repr__(self):
        """ The connection class representation is the value of the hostname property. """
        return self.hostname

    def get(self, url: str, payload: str = None, headers: dict = None) -> dict:
        """
        Send HTTPS GET request, using HTTPS protocol.
            
        Parameters:
        -----------
        url: string
            URL string used to construct the HTTPS request.
        payload: string
            Additional data used to construct the HTTPS request (Optional).
        headers: dict
            Additional header information (Optional).
        
        Return:
        -------
        jsonResponse: dict
            Return the date retrieved from the network device using HTTPS.
        """

        # Verify provided virables:
        self._verify(url, payload, headers)

        # Return the date retrieved from the network device using HTTPS.:
        return self._connection('GET', url, payload)

    def _verify(self, url, payload, headers) -> None:
        """ Verify provided virables. """

        # Verify if the specified url variable is a string:
        if url is not None and not isinstance(url, str):
            # Change connection status to False:
            self.status = False
            # Rais exception:
            raise TypeError('The provided url variable must be a string.')

        # Verify if the specified payload variable is a string:
        if payload is not None and not isinstance(payload, str):
            # Change connection status to False:
            self.status = False
            # Rais exception:
            raise TypeError('The provided payload variable must be a string.')

        if headers is not None:
            # Verify if the specified headers variable is a dictionary:
            if isinstance(headers, dict) or None:
                # Headers declaration:
                self.headers = headers
            else:
                # Change connection status to False:
                self.status = False
                # Rais exception:
                raise TypeError('The provided headers variable must be a dictionary.')

    def _connection(self, request_method, url, payload) -> dict:
        """ Connect to server using HTTPS protocol. """

        # Create URL Address from tamplate:
        request_url = f'https://{self.hostname}:{self.https_port}/{url}'

        # Create a default Cisco header if not specified:
        if self.headers is None:
            self.headers = {
                'Accept': 'application/yang-data+json',
                'Content-Type': 'application/yang-data+json',
            }

        # Add the token to the header, if provided:
        if self.token is not None:
            self.headers['x-token'] = self.token

        # Log the beginning of a new connection to the https server:
        ApiCon.logger.info('Starting a new Https connection.', self.task_id, self.device)

        # Start clock count:
        start_time = time.perf_counter()

        try: # Try to establish a connection to a network device:

            session = requests.Session()

            # Connect to the network device with password and username or by using token:
            if self.token is None:
                request = requests.Request(
                    request_method,
                    request_url,
                    headers=self.headers,
                    auth=(self.username, self.password),
                    data=payload,
                )
            else:
                request = requests.Request(
                    request_method,
                    request_url,
                    headers=self.headers,
                    data=payload,
                )

            prepare_request = session.prepare_request(request)
            response = session.send(
                prepare_request,
                verify=self.certificate,
            )

        except requests.exceptions.SSLError as error:
            ApiCon.logger.error(error, self.task_id, self.device)
            # Change connection status to False:
            self.status = False
            # Return connection starus:
            return self.status

        except requests.exceptions.Timeout as error:
            ApiCon.logger.error(error, self.task_id, self.device)
            # Change connection status to False:
            self.status = False
            # Return connection starus:
            return self.status

        except requests.exceptions.InvalidURL as error:
            ApiCon.logger.error(error, self.task_id, self.device)
            # Change connection status to False:
            self.status = False
            # Return connection starus:
            return self.status

        except requests.exceptions.ConnectionError as error:
            ApiCon.logger.error(error, self.task_id, self.device)
            # Change connection status to False:
            self.status = False
            # Return connection starus:
            return self.status

        else:

            # Log when https connection was established:
            ApiCon.logger.debug('Https connection was established.', self.task_id, self.device)

            # Finish clock count & method execution time:
            finish_time = time.perf_counter()
            self.execution_time = round(finish_time - start_time, 5)

            # Log time of command execution:
            if self.execution_time > 2:
                ApiCon.logger.debug(
                    f'HTTPS connection taken {self.execution_time} seconds.',
                    self.task_id, self.device, execution_time=self.execution_time
                )
            else:
                ApiCon.logger.debug(
                    f'HTTPS connection taken {self.execution_time} second.',
                    self.task_id, self.device, execution_time=self.execution_time
                )

            # Convert HTTPS response to dictionary:
            return self._check_response(response)

    def _check_response(self, response) -> dict:
        """ 
            Check type of HTTPS request response.
            If the response is correct, the response data will be converted to dictionary format.
        """

        # Collect response code:
        self.response_code = response.status_code

        # Check response status:
        if self.response_code < 200: # All respons from 0 to 199.
            ApiCon.logger.warning(
                f'Connection to {self.hostname}, was a informational HTTPS request. HTTPS response returned {response.status_code} code.',
                self.task_id, self.device
            )
            # Change connection status to True:
            self.status = True

        elif self.response_code < 300: # All respons from 200 to 299.
            ApiCon.logger.debug(
                f'Connection to {self.hostname}, was a success HTTPS request. HTTPS response returned {response.status_code} code.',
                self.task_id, self.device
            )
            # Change connection status to True:
            self.status = True

        elif self.response_code < 400: # All respons from 300 to 399.
            ApiCon.logger.warning(
                f'Connection to {self.hostname}, returned redirection HTTPS error. HTTPS response returned {response.status_code} code.',
                self.task_id, self.device
            )
            # Change connection status to False:
            self.status = False

        elif self.response_code < 500: # All respons from 400 to 499.
            ApiCon.logger.error(
                f'Connection to {self.hostname}, returned client HTTPS error. HTTPS response returned {response.status_code} code.',
                self.task_id, self.device
            )
            # Change connection status to False:
            self.status = False

        elif self.response_code < 600: # All respons from 500 to 599.
            ApiCon.logger.error(
                f'Connection to {self.hostname}, returned server HTTPS error. HTTPS response returned {response.status_code} code.',
                self.task_id, self.device
            )
            # Change connection status to False:
            self.status = False

        # Convert HTTPS response to Python dictionary:

        try: # Try to convert JSON response into a Python dictionary:

            # Convert JSON response into a Python dictionary:
            convertResponse = json.loads(response.text)
            # Change the status value of the JSON conversion process to True:
            self.json_status = True

        except:

            # Change the status value of the JSON conversion process to False:
            self.json_status = False

            try: # Try to convert XML response into a Python dictionary if JSON fails:
                # Convert XML response into a Python dictionary:
                convertResponse = xmltodict.parse(response.text)
                # Change the status value of the XML conversion process to True:
                self.xml_status = True
            except:
                # Change the status value of the XML conversion process to False:
                self.xml_status = False

        finally:

            if self.json_status is False and self.xml_status is False:
                # Log when python dictionary convert process fail:
                ApiCon.logger.warning(
                    'Python JSON and XML dictionary convert process fail.',
                    self.task_id, self.device
                )
                convertResponse = False
        
        # Return Https response in Json format:
        return convertResponse
