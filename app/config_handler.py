from pathlib import Path
from configparser import ConfigParser


class InvalidVanillaPathError(Exception):
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message
        super().__init__(message)


class InvalidModPathError(Exception):
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message
        super().__init__(message)


class ModPath(type(Path())):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if not self.exists():
            raise InvalidModPathError(
                title="Invalid mod path!",
                message="Couldn't find mod files!"
            )

        if not Path(str(self) + "\common").exists():
            print(str(self) + "\common")
            raise InvalidModPathError(
                title="Invalid mod path!",
                message="Couldn't find mod files!"
            )


class VanillaPath(type(Path())):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if not self.exists() or self == "":
            raise InvalidVanillaPathError(
                title="Invalid vanilla path!",
                message="Couldn't find vanilla files!"
            )
        if not Path(str(self) + "\common").exists():
            raise InvalidVanillaPathError(
                title="Invalid vanilla path!",
                message="Couldn't find vanilla files!"
            )


def create_new_config():
    config = ConfigParser()
    prefix = input("Enter mod prefix: ")
    config['SETTINGS'] = {
        "prefix": prefix,
        "mod_path": "null",
        "vanilla_path": "null"
    }
    with open('config/config.ini', 'w') as configfile:
        config.write(configfile)


def read_config():
    config = ConfigParser()
    while True:
        try:
            config.read('config/config.ini')
            mod_path = ModPath(config["SETTINGS"]["mod_path"])
            vanilla_path = VanillaPath(config["SETTINGS"]["vanilla_path"])
            break

        except InvalidVanillaPathError:
            config["SETTINGS"]["vanilla_path"] = input("Invalid vanilla path. Please enter a valid path: ")
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)

        except InvalidModPathError:
            config["SETTINGS"]["mod_path"] = input("Invalid Mod path. Please enter a valid path: ")
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)
    return config
