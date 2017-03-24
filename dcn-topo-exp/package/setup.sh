#!/bin/sh

# python setuptools must be installed to run. This can be installed as:
# sudo apt-get install -y python-setuptools
cd ripl && python setup.py develop
cd ../
cd riplpox && python setup.py develop
cd ../
cd jellyfish && python setup.py develop
