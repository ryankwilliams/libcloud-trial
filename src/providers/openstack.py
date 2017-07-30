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

    def images(self):
        """List images."""
        print('Fetching available images..')

        for item in self.driver.list_images():
            print(item.name)
