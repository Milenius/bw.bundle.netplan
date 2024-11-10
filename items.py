global node

actions = {
    'netplan-apply': {
        'command': "/usr/sbin/netplan apply",
        'expected_return_code': None,
        'needs': [
            'file:/etc/netplan/50-cloud-init.yaml', 
        ]
    }
}

files = {
    "/etc/netplan/50-cloud-init.yaml": {
        'source': "etc/netplan/50-cloud-init.yaml.j2",
        'context': {
            'config': node.metadata.get('interfaces'),
        },
        'content_type': 'jinja2',
        'mode': "0644",
        'owner': "root",
        'group': "root",
    },
}
