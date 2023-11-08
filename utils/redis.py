import redis
from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')

REDIS_HOST = configur.get('master_redis', 'redis_host')
REDIS_PORT = configur.get('master_redis', 'redis_port')
REDIS_PASSWORD = configur.get('master_redis', 'redis_password')

def get_master_client():
	_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None, decode_responses=True)
	return _redis_client

def get_redis_key(name:str, eVars:list, namespace:str="m", delim:str=":", version:int=1):
	return delim.join([namespace,name+str(version)] +list(eVars))