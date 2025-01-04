import re

global metadata_reactor, node, repo

def extract_route_from_option(option):
    """Extract route information from an 'up' option string."""
    if not option.startswith('up ip r add'):
        return None

    # Remove 'up ip r add' prefix
    route_str = option.replace('up ip r add ', '')

    # Initialize route dict
    route = {}

    # Extract network/mask
    # Try matching IP/mask first, then fall back to just IP
    network_match = re.match(r'(\d+\.\d+\.\d+\.\d+(?:/\d+)?)', route_str)

    if network_match:
        route['to'] = network_match.group(1)

    # Extract via (gateway)
    via_match = re.search(r'via (\d+\.\d+\.\d+\.\d+)', route_str)
    if via_match:
        route['via'] = via_match.group(1)
    else:
        route['via'] = None

    # Extract source
    src_match = re.search(r'src (\d+\.\d+\.\d+\.\d+)', route_str)
    if src_match:
        route['src'] = src_match.group(1)

    return route


def process_routes_from_options(options):
    """Process all route options and return list of route dictionaries."""
    routes = []
    for opt in options:
        if opt.startswith('up ip r add'):
            route = extract_route_from_option(opt)
            if route:
                routes.append(route)
    return routes


@metadata_reactor
def routes_from_options(metadata):
    """Main metadata reactor function."""
    # If no interfaces, return empty dict
    if 'interfaces' not in metadata:
        return {}

    # Initialize result dict
    result = {}

    # For each interface in the existing metadata
    for interface_name, interface in metadata.get('interfaces', {}).items():
        # Only process interfaces that have options but no routes
        if 'options' in interface and 'routes' not in interface:
            routes = process_routes_from_options(interface['options'])
            if routes:
                # Only add to result if we have routes to add
                result[interface_name] = {
                    'routes': routes
                }

    # Only return interfaces dict if we have changes
    return {'interfaces': result} if result else {}
