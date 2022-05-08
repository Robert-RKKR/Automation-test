PATH = 'static/ico/model/device/'

ICONS = (
    (0, (f'{PATH}switch.svg')),
    (1, (f'{PATH}border_router.svg')),
    (2, (f'{PATH}chassis.svg')),
    (3, (f'{PATH}console.svg')),
    (4, (f'{PATH}firewall.svg')),
    (5, (f'{PATH}router.svg')),
    (6, (f'{PATH}router_firewall.svg')),
    (7, (f'{PATH}router_wifi_1.svg')),
    (8, (f'{PATH}router_wifi_2.svg')),
    (9, (f'{PATH}stack.svg')),
    (10, (f'{PATH}stack_firewall_1.svg')),
    (11, (f'{PATH}stack_firewall_2.svg')),
    (12, (f'{PATH}switch.svg')),
    (13, (f'{PATH}wifi-connection.svg')),
    (14, (f'{PATH}wireless-router.svg')),
)

DEVICE_TYPE = (
    (0, ('Autodetect')),
    (1, ('Cisco IOS')),
    (2, ('Cisco IOS XE')),
    (3, ('Cisco IOS XR')),
    (4, ('Cisco NX OS')),
    (5, ('Cisco ASA')),
    (99, ('Unsupported')),
)

DEVICE_TYPE_NAPALM = {
    1: 'ios',
    2: 'iosxe',
    3: 'iosxr',
    4: 'nxos',
    5: 'asa',
}
