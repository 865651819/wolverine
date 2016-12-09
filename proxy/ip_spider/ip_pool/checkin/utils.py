import re


def is_valid_ip(ip):
    if not ip:
        return False
    valid_ip_address_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    pattern = re.compile(valid_ip_address_regex)
    return bool(pattern.match(ip))


def is_valid_port(port):
    if not port:
        return False
    valid_port_regex = "^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
    pattern = re.compile(valid_port_regex)
    return bool(pattern.match(port))
