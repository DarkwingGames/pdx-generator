
from config_handler import *

config = ConfigParser()

if not Path("config/config.ini").exists():
    create_new_config()
    config = read_config()
else:
    config = read_config()
    print(config)