import os

system = 'cisco_ios'
text = ' show ip interfece brief'
command = text.strip().replace(' ', '_')
output = f'{system}_{command}'

print(output)
