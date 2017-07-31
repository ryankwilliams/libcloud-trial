"""OpenStack module using libcloud to interface with OpenStack."""
import libcloud.security
import yaml
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

PROVIDER = 'openstack'


class Authentication(object):
    """Authentication class."""

    def __init__(self, auth_file):
        """Constructor.
        :param auth_file: Authentication information set by file.
        :type auth_file: bool
        """
        self._driver = None

        # ignore SSL
        libcloud.security.VERIFY_SSL_CERT = False

        if auth_file:
            print('Fetching authentication by file %s.' % auth_file)

            # load authentication file
            with open(auth_file, 'r') as f:
                data = yaml.load(f)

            try:
                # establish authentication with provider
                self.driver = get_driver(Provider.OPENSTACK)(
                    data[PROVIDER]['username'],
                    data[PROVIDER]['password'],
                    ex_tenant_name=data[PROVIDER]['tenant'],
                    ex_force_auth_url=data[PROVIDER]['url'],
                    ex_force_auth_version='2.0_password'
                )
            except KeyError as ex:
                raise KeyError(
                    '%s is missing from %s' % (ex.message, auth_file)
                )
        else:
            print('Fetching authentication by environment variables.')
            raise NotImplementedError('Env vars not supported yet.')

        print('Successfully establish authentication with %s provider.' %
              PROVIDER)

    @property
    def driver(self):
        """Return driver object."""
        return self._driver

    @driver.setter
    def driver(self, value):
        """Set driver object.
        :param value: Driver instance.
        :type value: object
        """
        self._driver = value


class OpenStack(Authentication):
    """OpenStack class."""

    def __init__(self, auth_file=None):
        """Constructor."""
        super(OpenStack, self).__init__(auth_file)

    @property
    def nodes(self):
        """Return list of nodes."""
        return self.driver.list_nodes()

    @property
    def images(self):
        """Return list of images."""
        return self.driver.list_images()

    @property
    def sizes(self):
        """Return list of sizes."""
        return self.driver.list_sizes()

    @property
    def networks(self):
        """Return list of networks."""
        return self.driver.ex_list_networks()

    def image_lookup(self, name, raises=False):
        """Image lookup to fetch image object.
        :param name: Image name.
        :type name: str
        :param raises: Raise exception if image not found.
        :type raises: bool
        :return: Image object.
        :rtype: object
        """
        data = filter(lambda elm: elm.name == name, self.images)
        if len(data) == 0:
            if raises:
                raise Exception('Image %s not found!' % name)
            return None
        else:
            return data[0]

    def size_lookup(self, name, raises=False):
        """Lookup size object based on size given.
        :param name: Image name.
        :type name: str
        :param raises: Raise exception if size not found.
        :type raises: bool
        :return: Image object.
        :rtype: object
        """
        data = filter(lambda elm: elm.name == name, self.sizes)
        if len(data) == 0:
            if raises:
                raise Exception('Size %s not found!' % name)
            return None
        else:
            return data[0]

    def network_lookup(self, name, raises=False):
        """Lookup network object based on network given.
        :param name: Network name.
        :type name: str
        :param raises: Raise exception if network not found.
        :type raises: bool
        :return: Network object.
        :rtype: list
        """
        data = filter(lambda elm: elm.name == name, self.networks)
        if len(data) == 0:
            if raises:
                raise Exception('Network %s not found!' % name)
            return None
        else:
            return data

    def node_lookup(self, name, raises=False):
        """Lookup node object based on node given.
        :param name: Node name.
        :type name: str
        :param raises: Raise exception if node not found.
        :type raises: bool
        :return: Node object.
        :rtype: object
        """
        data = filter(lambda elm: elm.name == name, self.nodes)
        if len(data) == 0:
            if raises:
                raise Exception('Node %s not found!' % name)
            return None
        else:
            return data[0]

    def associate_floating_ip(self):
        """Associate floating ip to node."""
        raise NotImplementedError

    def disassociate_floating_ip(self):
        """Disassociate floating ip from node."""
        raise NotImplementedError

    def create(self, name, image, size, network):
        """Create node.
        :param name: Node name.
        :type name: str
        :param image: Image name.
        :type image: str
        :param size: Flavor size name.
        :type size: str
        :param network: Network name.
        :type network: str
        """
        # Lookup image object
        _image = self.image_lookup(image, raises=True)

        # Lookup size object
        _size = self.size_lookup(size, raises=True)

        # Lookup network object
        _network = self.network_lookup(network, raises=True)

        # Create node
        node = self.driver.create_node(
            name=name,
            image=_image,
            size=_size,
            networks=_network
        )

        # Wait for node to finish building
        self.driver.wait_until_running([node])

        # TODO: Associate floating ip
        # self.associate_floating_ip()

    def delete(self, name):
        """Delete node.
        :param name: Node name.
        :type name: str
        """
        # Lookup node object
        _node = self.node_lookup(name, raises=True)

        # TODO: Disassociate floating ip

        # Delete node
        self.driver.destroy_node(_node)
