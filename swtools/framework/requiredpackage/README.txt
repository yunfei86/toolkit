The packages ordereddict-1.1-tar.gz and unittest2-0.5.1.tar.gz are
reqired for this framework to function properly.

To unpack please use the following commands:

tar -xvzf ordereddict-1.1.tar.gz
tar -xvzf unittest2-0.5.1.tar.gz

After unpacking cd in to the respective directories and install them.

To install ordereddict-1.1.tar.gz you have to

cd ordereddict-1.1
sudo python setup.py build
sudo python setup.py install

To install unittest2-0.5.1.tar.gz you have to

cd unittest2-0.5.1
sudo python setup.py build
sudo python setup.py install

This will install both the packages. This should be done prior to using the package.