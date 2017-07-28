from distutils.core import setup
from setuptools import find_packages

setup(
    name='gdaxcli',
    packages=find_packages('gdaxcli', exclude=['tests']),
    version='0.1.0',
    description='Commandline client for trading on GDAX',

    author='Son Pham',
    author_email='sp@sonpham.me',
    url='https://github.com/sonph/gdaxcli',
    download_url='https://github.com/sonph/gdaxcli/archive/0.1.0.zip',
    license='MIT',

    keywords='gdax trading cryptocurrency bitcoin ethereum',
    install_requires=[
      # TODO: sync this with requirements.txt
      "gdax",
      "tabulate",
      "colorama",
    ],
    classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for
      #  'Intended Audience :: Developers',
      #  'Topic :: Software Development :: Build Tools',

      # Pick your license as you wish (should match "license" above)
       'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      #  'Programming Language :: Python :: 2',
      #  'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      #  'Programming Language :: Python :: 3',
      #  'Programming Language :: Python :: 3.2',
      #  'Programming Language :: Python :: 3.3',
      #  'Programming Language :: Python :: 3.4',
    ],
)

# For reference: https://packaging.python.org/tutorials/distributing-packages/
# Python package management is a PITA.
