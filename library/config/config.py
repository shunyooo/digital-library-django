import os
import configparser
config = configparser.ConfigParser()

def read_config():
	global config
	path_list = ['./config/config.ini', '../config/config.ini']
	for path in path_list:
		if os.path.exists(path):
			print(f'read config → {path}')
			config.read(path)
	return config

read_config()