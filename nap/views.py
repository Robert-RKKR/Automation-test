# Django Import:
from django.shortcuts import render

# Application Import:
from logger.logger import Logger
from autocore.netcon import NetCon

# Model Import:
from inventory.models.device import Device

# Celery Import:
from celery import shared_task
from automation.celery import app

# Logger initialization:
logger = Logger('Page')

@shared_task(bind=True, track_started=True, name='Test task')
def test_task(self) -> bool:
    logger.info('Test celery task done :)')
    print('Test celery task done :)')


# Views:
def automation(request, pk):

    logger.info('Hello, welcome on RKKR page :)')

    # Collect data to display:
    data = {
        'output': 'Test RKKR',
        'log': '',
    }

    # test_device = Device.objects.get(id=1)
    # connection = NetCon(test_device, 'ei930u29eikdj', 2)
    # data['output'] = connection.enabled_commands(['show version', 'show ip int brief'])
    # data['output'] = connection.configuration_commands([
    #     'hostname RKKR', 'no ip domain name'
    # ])
    # connection.close()

    test_task.delay()
    
    # GET method:
    return render(request, 'basic.html', data)
