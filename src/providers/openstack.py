"""OpenStack module using libcloud to interface with OpenStack."""
import libcloud.security
import urllib3
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

        # suppress insecure request warning messages
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        if auth_file:
            print('Fetching authentication by file %s.' % auth_file)

            # load authentication file
            with open(auth_file, 'r') as f:
                data = yaml.load(f)

            try:
                # establish authentication with provider
                self._driver = get_driver(Provider.OPENSTACK)(
                    data[PROVIDER]['username'],
                    data[PROVIDER]['password'],
                    ex_tenant_name=data[PROVIDER]['tenant'],
                    ex_force_auth_url=data[PROVIDER]['url'],
                    ex_force_auth_version='2.0_password',
                    ex_force_service_region=data[PROVIDER]['region']
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
        self._floating_ip = object
        self._key_pair = object

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
        """Return floating ip pool object."""
        return self._floating_ip_pool

    @floating_ip_pool.setter
    def floating_ip_pool(self, floating_ip_pool):
        """Set network object.

        :param floating_ip_pool: Floating ip pool object.
        :type floating_ip_pool: object
        """
        self._floating_ip_pool = floating_ip_pool

    @property
    def key_pair(self):
        """Return key pair."""
        return self._key_pair

    @key_pair.setter
    def key_pair(self, key_pair):
        """Set key pair object.

        :param key_pair: Key pair object.
        :type key_pair: object
        """
        self._key_pair = key_pair

    @property
    def floating_ip(self):
        """Return floating ip object."""
        return self._floating_ip

    @floating_ip.setter
    def floating_ip(self, floating_ip):
        """Set network object.

        :param floating_ip: Floating ip object.
        :type floating_ip: object
        """
        self._floating_ip = floating_ip

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

    @property
    def key_pairs(self):
        """Return list of key pairs."""
        return self.driver.list_key_pairs()

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
        """Lookup floating ip pool object based on floating ip pool name.

        :param name: Floating ip pool name.
        :type name: str
        """
        data = filter(lambda elm: elm.name == name, self.floating_ip_pools)
        if len(data) == 0:
            raise Exception('Floating ip pool %s not found!' % name)
        else:
            self.floating_ip_pool = data[0]

    def key_pair_lookup(self, name):
        """Lookup key pair object based on key pair name given.

        :param name: Key pair name.
        :type name: str
        """
        # no key pair to lookup
        if not name:
            return

        data = filter(lambda elm: elm.name == name, self.key_pairs)
        if len(data) == 0:
            raise Exception('Key pair %s not found!' % name)
        else:
            self.key_pair = data[0]

    def floating_ip_lookup(self):
        """Lookup floating ip for a node."""
        address = None

        for key in self.node.extra['addresses']:
            for network in self.node.extra['addresses'][key]:
                # skip if network is not type floating
                if network['OS-EXT-IPS:type'] != 'floating':
                    continue
                self.floating_ip = network['addr']
                break

        if not self.floating_ip:
            raise Exception('Unable to get floating ip for node!')

    def associate_floating_ip(self, floating_ip_pool):
        """Associate floating ip to node."""
        # Lookup floating ip pool object
        self.floating_ip_pool_lookup(floating_ip_pool)

        # create floating ip within pool
        float_ip = self.floating_ip_pool.create_floating_ip()

        # attach floating ip to node
        self.driver.ex_attach_floating_ip_to_node(self.node, float_ip)

    def disassociate_floating_ip(self):
        """Disassociate floating ip from node."""
        # lookup floating ip for node
        self.floating_ip_lookup()

        # get floating ip object
        float_ip = self.driver.ex_get_floating_ip(self.floating_ip)

        # detach floating ip from node
        self.driver.ex_detach_floating_ip_from_node(self.node, float_ip)

        # delete floating ip
        self.driver.ex_delete_floating_ip(float_ip)

    def create(self, name, image, size, network, floating_ip_pool,
               key_pair=None):
        """Create node.
        :param name: Node name.
        :type name: str
        :param image: Image name.
        :type image: str
        :param size: Flavor size name.
        :type size: str
        :param network: Network name.
        :type network: str
        :param floating_ip_pool: Floating ip pool name.
        :type floating_ip_pool: str
        :param key_pair: Name of the key pair to inject into node.
        :type key_pair: str
        """
        # lookup image object
        self.image_lookup(image)

        # lookup size object
        self.size_lookup(size)

        # lookup network object
        self.network_lookup(network)

        # create node
        if key_pair:
            # with key pair
            self.node = self.driver.create_node(
                name=name,
                image=self.image,
                size=self.size,
                networks=self.network,
                ex_keyname=key_pair
            )
        else:
            # without key pair
            self.node = self.driver.create_node(
                name=name,
                image=self.image,
                size=self.size,
                networks=self.network
            )

        # wait for node to finish building
        self.driver.wait_until_running([self.node])

        # associate floating ip with node
        self.associate_floating_ip(floating_ip_pool)

    def delete(self, name):
        """Delete node.
        :param name: Node name.
        :type name: str
        """
        # lookup node object
        self.node_lookup(name)

        # dissociate floating ip from node
        self.disassociate_floating_ip()

        # delete node
        self.driver.destroy_node(self.node)
