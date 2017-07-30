# libcloud-poc

The primary objective for this repository is to evaluate the use of apache
libcloud to perform requests in various providers. Most cloud providers provide
some way to interface with it (RESTful API, SDK, command line interface). When
working on a project that requires the use of multiple providers, this grows
your projects dependencies with each cloud provider libraries. By installing
apache libcloud, it installs itself and only a couple packages it depends on.
While providing a huge list of providers to interface with. Having apache
libcloud installed in your project would decrease the need for many packages
by replacing it with one.

The end goal is to compare how it is using apache libcloud to perform the same
type of requests using a providers SDK libraries. If it is transparent, it
should allow you to easily switch to using apache libcloud within your project.

# repository structure

Within this repository you will find a python package named **src/providers**.
This package holds modules for all different providers
(authentication and SDK classes) These classes are to provide a simple way to
perform various requests in that given provider. There is also an **examples**
folder which contains example input files to perform some interactions with the
provider of its choice.

# environment setup

To use these modules, you will want to create a Python virtual environment and
install the packages defined in requirements.txt.