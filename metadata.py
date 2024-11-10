@metadata_reactor
def enable_iptables_systemd(metadata):
    if not node.has_bundle('iptables'):
        raise DoNotRunAgain

    return {
        'iptables': {
            'systemd': True,
        },
    }
