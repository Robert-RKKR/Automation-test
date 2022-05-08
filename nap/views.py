# Django Import:
import time
from django.shortcuts import render

# Application Import:
from logger.logger import Logger
from autocore.connections.netcon import NetCon

# Model Import:
from inventory.models.device import Device

# Celery Import:
from celery import shared_task
from automation.celery import app
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Channels variable:
channel_layer = get_channel_layer()

# Logger initialization:
logger = Logger('Page')

@shared_task(bind=True, track_started=True, name='Test task')
def test_task(self) -> bool:
    
    output = []
    test_device = Device.objects.get(id=1)
    connection = NetCon(test_device, self.request.id)
    output.append(connection.enabled_commands(['show version', 'show ip int brief']))
    output.append(connection.configuration_commands(['hostname RKKR', 'no ip domain name']))
    connection.close_connection()

    async_to_sync(channel_layer.group_send)('collect', {'type': 'send_collect', 'text': str(output)})
    return output


# Views:
def automation(request, commands):

    logger.info('Hello, welcome on RKKR page :)')

    # Collect data to display:
    data = {
        'output': 'Test RKKR',
        'log': '',
    }

    # test_device = Device.objects.get(id=1)
    # connection = NetCon(test_device, 'ei930u29eikdj', 2)
    # data['output'] = connection.enabled_commands(['show version', 'show ip int brief'])
    # data['output'] = connection.configuration_commands(['hostname RKKR', 'no ip domain name'])
    # connection.close()

    # test_task.delay([
    #     'show version',
    #     'show ip interface brief',
    #     'show interface description'
    # ])


    commands = commands.split('_')
    commands = ' '.join(commands)
    data['output'] = test_task.delay()

    # test_device = Device.objects.get(id=1)
    # connection = NetCon(test_device)
    # data['output'] = connection.enabled_commands(commands)
    # data['output'] = connection.configuration_commands(['hostname RKKR', 'no ip domain name'])
    # connection.close_connection()
    
    # GET method:
    return render(request, 'basic.html', data)
