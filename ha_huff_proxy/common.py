import ipaddress


def is_valid_ipv4(ip):
    try:
        # Attempt to create an IPv4 address object
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False
