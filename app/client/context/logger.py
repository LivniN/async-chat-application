import logging
from app.client.context import config

format = '%(asctime)s %(name)s %(levelname)s %(message)s'
level = config['logger']['level']
logging.basicConfig(format=format, level=level)
log = logging.getLogger('clinet')
