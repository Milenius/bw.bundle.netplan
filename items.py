from bundlewrap.utils.text import mark_for_translation as _

def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

files = {
    "/etc/netplan/50-cloud-init.yaml": {
        'source': "etc/netplan/50-cloud-init.yaml.j2",
        'context': {
            'config': node.metadata.get('interfaces'),
        },
        'content_type': 'jinja2',
        'filters': {
            'netmask_to_cidr': netmask_to_cidr,
        },
        'mode': "0644",
        'owner': "root",
        'group': "root",
    },
}

actions = {
    'netplan-apply': {
        'command': "/usr/sbin/netplan apply",
        'expected_return_code': None,
        'needs': [
            'file:/etc/netplan/50-cloud-init.yaml', 
        ]
    }
}