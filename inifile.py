import configparser,os

path = os.path.abspath('.') + '\config.ini'
config = configparser.ConfigParser()
config.read(path)
name = config.get('base', 'name')
password = config.get('base', 'password')
Appium_ip=config.get('base', 'Appium_ip')
And_ip=config.get('base', 'And_ip')

