import napalm


driver = napalm.get_network_driver('iosxr')

# ios, 

try:
    connection = driver(
        hostname='sandbox-iosxe-latest-1.cisco.com',
        username='developer',
        password='C1sco12345',
        optional_args={'port': 22},
    )
    connection.open()
except napalm.base.exceptions.ConnectionException as error:
    print(error)
    
print(connection.get_facts())
# print(connection.get_interfaces_ip())

# print(connection.cli(['show mac-address']))
# print(connection.get_mac_address_table()())
# print(connection.get_mac_address_table())

# connection.load_merge_candidate(filename='autocore/comands.conf')
# connection.load_merge_candidate(config='hostname test\ninterface Ethernet2\ndescription bla')
# print(connection.compare_config())

# while(True):
#     output = input('Are you happy? y/n: ')
#     if output == 'y':
#         connection.commit_config()
#         print('Changes accepted!')
#         break
#     elif output == 'n':
#         connection.discard_config()
#         print('Changes discarded!')
#         break
