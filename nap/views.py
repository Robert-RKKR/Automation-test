# Django Import:
from django.shortcuts import render

# Application Import:
from logger.logger import Logger
from autocore.netcon import NetCon

# Model Import:
from inventory.models.device import Device

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

    test_device = Device.objects.get(id=1)
    connection = NetCon(test_device, 'ei930u29eikdj', 2)
    data['output'] = connection.send_commands(['show version', 'show ip int brief'])
    
    # GET method:
    return render(request, 'basic.html', data)
