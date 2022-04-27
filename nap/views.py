# Django Import:
from django.shortcuts import render

# Application Import:
from logger.logger import Logger

# Logger initialization:
logger = Logger('Page')

# Views:
def automation(request, pk):

    logger.info('Hello, welcome on RKKR page :)')

    # Collect data to display:
    data = {
        'output': 'Test RKKR',
        'log': '',
    }
    
    # GET method:
    return render(request, 'basic.html', data)
