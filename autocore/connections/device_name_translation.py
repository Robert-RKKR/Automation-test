# Supported device type:
CISCO_IOS = {
    'repr': 'Cisco IOS',
    'commands': 'cisco_ios',
    'netmiko': 'cisco_ios',
    'napalm': 'ios'
}
CISCO_XE = {
    'repr': 'Cisco XE',
    'commands': 'cisco_ios',
    'netmiko': 'cisco_xe',
    'napalm': 'ios'
}
CISCO_XR = {
    'repr': 'Cisco XR',
    'commands': 'cisco_xr',
    'netmiko': 'cisco_xr',
    'napalm': 'iosxr'
}
CISCO_NXOS = {
    'repr': 'Cisco NXOS',
    'commands': 'cisco_nxos',
    'netmiko': 'cisco_nxos',
    'napalm': 'nxos'
}
CISCO_ASA = {
    'repr': 'Cisco ASA',
    'commands': 'cisco_asa',
    'netmiko': 'cisco_asa'
}
CISCO_WLC = {
    'repr': 'Cisco WLC',
    'commands': 'cisco_wlc'
}

# Device type model variables:
DEVICE_TYPE = (
    (0, ('Autodetect')),
    (1, (CISCO_IOS['repr'])),
    (2, (CISCO_XE['repr'])),
    (3, (CISCO_XR['repr'])),
    (4, (CISCO_NXOS['repr'])),
    (5, (CISCO_ASA['repr'])),
    (6, (CISCO_WLC['repr'])),
    (99, ('Unsupported')),
)

# Device type ID to name translation:
DEVICE_TYPE_ID = {
    1: CISCO_IOS,
    2: CISCO_XE,
    3: CISCO_XR,
    4: CISCO_NXOS,
    5: CISCO_ASA,
    6: CISCO_WLC,
}

# Device name translation functions:
def collect_device_name_from_id(device_type_id: int, netmiko: bool = False, napalm: bool = False):
    
    # Check version of device type name:
    if netmiko:
        return DEVICE_TYPE_ID.get(device_type_id, {}).get('netmiko', False)
    elif napalm:
        return DEVICE_TYPE_ID.get(device_type_id, {}).get('napalm', False)
    else:
        pass

def collect_device_id_from_name(device_type_name: str, netmiko: bool = False, napalm: bool = False):

    def search_loop(version):
        for id in DEVICE_TYPE_ID:
            current_device_type = DEVICE_TYPE_ID[id]
            current_device_type_name = current_device_type.get(version, False)
            if current_device_type_name == device_type_name:
                return id
    
    # Check version of device type name:
    if netmiko:
        return search_loop('netmiko')
    elif napalm:
        return search_loop('napalm')
    else:
        pass
