from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'iot_services_sdk',         
  packages = ['iot_services_sdk'],   
  version = '2.0.2',
  license='SAP Sample Code License',        
  description = 'SDK for SAP IoT Services on Cloud Foundry. Wraps all Device Management APIs as well as both Cloud Gateways.',  
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  python_requires='>=3',
  author = 'Philipp Steinrötter',                  
  author_email = 'philipp.steinroetter@sap.com',     
  url = 'https://github.com/SAP/iot-services-sdk',   
  keywords = 'SAP IoT Services CF SDK MQTT REST Device Management Internet of Things',
  download_url='https://github.com/SAP/iot-services-sdk/archive/1.0.tar.gz',
  install_requires=['paho-mqtt', 'requests'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      
    'Intended Audience :: Developers',   
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)