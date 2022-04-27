from napalm import get_network_driver

driver = get_network_driver('ios')
device = driver(
    hostname='sandbox-iosxe-latest-1.cisco.com',
    username='developer',
    password='C1sco12345',
    optional_args={'port': 22},
)
device.open()
device.load_merge_candidate(filename='autocore/comands.conf')
#device.load_merge_candidate(config='hostname test\ninterface Ethernet2\ndescription bla')
print(device.compare_config())

while(True):
    output = input('Are you happy? y/n: ')
    if output == 'y':
        device.commit_config()
        print('Changes accepted!')
        break
    elif output == 'n':
        device.discard_config()
        print('Changes discarded!')
        break
