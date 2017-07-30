"""Example usage of OpenStack libcloud."""
from providers import OpenStack

if '__main__' == __name__:
    obj = OpenStack('../examples/auth.yml')
    obj.images()
