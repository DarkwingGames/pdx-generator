import json
# TODO make adding new config items less work
from json import JSONDecodeError
from pydantic import BaseModel, validator, ValidationError
from pathlib import Path

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

class Config(BaseModel):
    """
    Basic Model to validate the data in the config file.

    Attributes
    -----------
    prefix: the mod prefix
    vanilla_path: the path to the vanilla stellaris root folder
    mod_path: the path to the mod root folder
    """
    prefix: str
    vanilla_path: Path
    mod_path: Path

    def create_new:
        new_config = {
            "prefix": "",
            "vanilla_path": "",
            "mod_path": ""
        }


    @validator("vanilla_path")
    @classmethod
    def validate_vanilla_path(cls, vanilla_path):
        if not Path(vanilla_path).exists or not Path(str(vanilla_path) + "\common").exists():
            raise InvalidVanillaPathError(
                title=vanilla_path,
                message="Couldn't find vanilla files!"
            )




    @validator("mod_path")
    @classmethod
    def validate_mod_path(cls, mod_path):
        if not Path(mod_path).exists() or not Path(str(mod_path) + "\common").exists():
            raise InvalidModPathError(
                title=mod_path,
                message="Couldn't find mod files!"
            )


    class Config:
        validate_assignment = True

def read_config(file):
    while True:

        if Path(file).exists():
            try:
                config = Config.parse_file(file)
            except(JSONDecodeError):
                print("Config file missing or corrupted, generating new file.")
                new_prefix = input("Enter mod prefix:")
                new_vanilla_path = Path(input("Enter path to vanilla root folder: "))
                new_mod_path = Path(input("Enter path to mod root folder: "))
                new_config = Config(prefix=new_prefix, vanilla_path=new_vanilla_path, mod_path=new_mod_path)
                with open(file, "w") as config_file:
                    print(new_config.schema())
                    config_file.write(new_config.schema())

            break
        else:
            new_empty_config = Config(prefix="", vanilla_path="", mod_path="")
            print(new_empty_config)
            print("Config file missing or corrupted, generating new file.")
            with open(file, "w") as config_file:
                config_file.write(new_empty_config.schema())
            continue


    #return config
