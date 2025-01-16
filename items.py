from bundlewrap.utils.text import mark_for_translation as _

def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

files = {
    "/etc/netplan/50-cloud-init.yaml": {
        'source': "etc/netplan/50-cloud-init.yaml.j2",
        'context': {
            'interfaces': dict(sorted(node.metadata.get('interfaces', {}).items())),
        },
        'content_type': 'jinja2',
        'mode': "0640",
        'owner': "root",
        'group': "root",
        'triggers': [
            'action:netplan-apply',
        ],
    },
}

actions = {
    'netplan-apply': {
        'command': "/usr/sbin/netplan apply",
        'expected_return_code': None,
        'needs': [
            'file:/etc/netplan/50-cloud-init.yaml',
        ],
        'triggered': True,
    }
}
