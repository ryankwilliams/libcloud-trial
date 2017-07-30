"""Example usage of OpenStack libcloud."""
from providers import OpenStack
import time

if '__main__' == __name__:
    obj = OpenStack('../examples/auth.yml')

    node = 'node1'
    image = ''
    flavor_size = 'm1.small'
    internal_network = ''

    obj.create(
        node,
        image,
        flavor_size,
        internal_network
    )

    time.sleep(10)

    obj.delete(node)
