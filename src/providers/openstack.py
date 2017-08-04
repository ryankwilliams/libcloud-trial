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
        self._driver = object

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
        self._node = object
        self._image = object
        self._size = object
        self._network = object
        self._floating_ip_pool = object

    @property
    def node(self):
        """Return node."""
        return self._node

    @node.setter
    def node(self, node):
        """Set node object.

        :param node: Node object.
        :type node: object
        """
        self._node = node

    @property
    def image(self):
        """Return image."""
        return self._image

    @image.setter
    def image(self, image):
        """Set image object.

        :param image: Image object.
        :type image: object
        """
        self._image = image

    @property
    def size(self):
        """Return size (flavor)."""
        return self._size

    @size.setter
    def size(self, size):
        """Set size (flavor) object.

        :param size: Size object.
        :type size: object
        """
        self._size = size

    @property
    def network(self):
        """Return network."""
        return self._network

    @network.setter
    def network(self, network):
        """Set network object.

        :param network: Network object.
        :type network: object
        """
        self._network = network

    @property
    def floating_ip_pool(self):
        """Return floating IP pool object."""
        return self._floating_ip_pool

    @floating_ip_pool.setter
    def floating_ip_pool(self, floating_ip_pool):
        """Set network object.

        :param floating_ip_pool: Floating IP pool object.
        :type floating_ip_pool: object
        """
        self._floating_ip_pool = floating_ip_pool

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

    @property
    def floating_ip_pools(self):
        """Return list of floating ip pools."""
        return self.driver.ex_list_floating_ip_pools()

    def image_lookup(self, name):
        """Image lookup to fetch image object.
        :param name: Image name.
        :type name: str
        """
        data = filter(lambda elm: elm.name == name, self.images)
        if len(data) == 0:
            raise Exception('Image %s not found!' % name)
        else:
            self.image = data[0]

    def size_lookup(self, name):
        """Lookup size object based on size given.
        :param name: Image name.
        :type name: str
        """
        data = filter(lambda elm: elm.name == name, self.sizes)
        if len(data) == 0:
            raise Exception('Size %s not found!' % name)
        else:
            self.size = data[0]

    def network_lookup(self, name):
        """Lookup network object based on network given.
        :param name: Network name.
        :type name: str
        """
        data = filter(lambda elm: elm.name == name, self.networks)
        if len(data) == 0:
            raise Exception('Network %s not found!' % name)
        else:
            self.network = data

    def node_lookup(self, name):
        """Lookup node object based on node given.
        :param name: Node name.
        :type name: str
        """
        data = filter(lambda elm: elm.name == name, self.nodes)
        if len(data) == 0:
            raise Exception('Node %s not found!' % name)
        else:
            self.node = data[0]

    def floating_ip_pool_lookup(self, name):
        """Lookup floating IP pool object based on floating ip pool name.
        :param name: Floating IP pool name.
        :type name: str
        """
        data = filter(lambda elm: elm.name == name, self.floating_ip_pools)
        if len(data) == 0:
            raise Exception('Floating IP pool %s not found!' % name)
        else:
            self.floating_ip_pool = data[0]

    def associate_floating_ip(self, floating_ip_pool):
        """Associate floating ip to node."""
        # Lookup floating IP pool object
        self.floating_ip_pool_lookup(floating_ip_pool)

        # Create floating IP within pool
        float_ip = self.floating_ip_pool.create_floating_ip()

        # Attach floating IP to node
        self.driver.ex_attach_floating_ip_to_node(self.node, float_ip)

    def disassociate_floating_ip(self):
        """Disassociate floating ip from node."""
        raise NotImplementedError

    def create(self, name, image, size, network, floating_ip_pool):
        """Create node.
        :param name: Node name.
        :type name: str
        :param image: Image name.
        :type image: str
        :param size: Flavor size name.
        :type size: str
        :param network: Network name.
        :type network: str
        :param floating_ip_pool: Floating IP pool name.
        :type floating_ip_pool: str
        """
        # Lookup image object
        self.image_lookup(image)

        # Lookup size object
        self.size_lookup(size)

        # Lookup network object
        self.network_lookup(network)

        # Create node
        self.node = self.driver.create_node(
            name=name,
            image=self.image,
            size=self.size,
            networks=self.network
        )

        # Wait for node to finish building
        self.driver.wait_until_running([self.node])

        self.associate_floating_ip(floating_ip_pool)

    def delete(self, name):
        """Delete node.
        :param name: Node name.
        :type name: str
        """
        # Lookup node object
        self.node_lookup(name)

        # TODO: Disassociate floating ip
        # self.disassociate_floating_ip()

        # Delete node
        self.driver.destroy_node(self.node)
