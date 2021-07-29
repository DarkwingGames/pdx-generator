import itertools
import re
import os
import json

from configparser import ConfigParser  # config file management
from pathlib import Path  # file path management
from dataclasses import dataclass  # dataclasses are easier to handle than regular classes

# GLOBAL VARIABLES_____________________________________________________________________________________________________

config_filename: str = "leader_system_config.ini"  # name of the config file

# CLASSES DEALING WITH CONFIGURATION___________________________________________________________________________________
@dataclass
class CustomConfig(ConfigParser):  # inheriting from ConfigParser so we can store out config values easier
    """
    Creates and validates the configuration file for the script generator

    Attributes
    ----------
    prefix : str
    The prefix used in your mods code
    vanilla_path: Path
    The path to your vanilla root folder
    mod_path: Path
    The path to your mod root folder

    """

    prefix: str = None  # mod prefix
    vanilla_path: Path = None  # path to vanilla stellaris root folder
    mod_path: Path = None  # path to mod root folder

    def __post_init__(self, *args, **kwargs):
        """
        Initialising ConfigParser so we can use it's features in this class

        """
        super().__init__(*args, **kwargs)

    def get_user_input(self) -> None:  # separate validation from input?
        """
        Query the user for information and check if it's valid

        """

        self.prefix = input("Enter mod prefix: ")  # Ask the user
        while self.prefix is None or type(self.prefix) != str:  # Check if user input is valid
            print("Invalid mod prefix, please enter a valid prefix. ")  # if not, keep asking
            self.prefix = input("Enter mod prefix: ")

        self.vanilla_path = Path(input("Enter path to vanilla root folder: "))
        while not self.vanilla_path.exists() or not Path(str(self.vanilla_path) + "\common").exists():
            print("Invalid vanilla path, please enter a valid path. ")
            self.vanilla_path = Path(input("Enter path to vanilla root folder: "))

        self.mod_path = Path(input("Enter path to mod root folder: "))
        while not self.mod_path.exists() or not Path(str(self.mod_path) + "\common").exists():
            print("Invalid mod path, please enter a valid path. ")
            self.mod_path = Path(input("Enter path to mod root folder: "))

    def set_config(self) -> None:
        """
        Assign user input values to config values

        Returns
        -------
        None
        """

        self["PREFIX"] = {  # map the answers to the config values
            "prefix": self.prefix
        }
        self["PATHS"] = {
            "vanilla_path": self.vanilla_path,
            "mod_path": self.mod_path,
        }

    def is_valid(self) -> bool:  # NOTE TO SELF: move to separate class? # can this be made more flexible?
        """
        Validate the existing configuration values. Raises an InvalidConfigError when encountering an invalid config file.

        Returns
        -------
        bool
            A boolean, telling wether the config file was found to be valid or not
        """
        if (
                self["PREFIX"]["prefix"] is None or type(
            self["PREFIX"]["prefix"]) != str  # check if the values in the config file are valid
                or not Path(
            self["PATHS"]["vanilla_path"]).exists()  # check if the files exist at the specified filepath
                or not Path(self["PATHS"]["vanilla_path"] + "\common").exists()
                or not Path(self["PATHS"]["mod_path"]).exists()
                or not Path(self["PATHS"]["mod_path"] + "\common").exists()

        ):
            raise InvalidConfigError()  # raise an error if not
            return False

        else:
            return True

    def write_config_ini(self) -> None:
        """Write the configuration values to the configuration file

        Returns
        -------
        None
        """

        with open(config_filename, 'w') as conf:
            self.write(conf)


# ERRORS_______________________________________________________________________________________________________________
class InvalidConfigError(Exception):
    """Raised when an invalid configuration file is encountered"""
    pass


class InvalidLeaderClassError(Exception):
    """Raised when an invalid leader class is encountered"""
    pass


# CLASSES DEALING WITH SCRIPT GENERATION_______________________________________________________________________________

@dataclass
class PdxScriptObject:
    supported_script_objects = []

    def __init_subclass__(cls, **kwargs):  # register existing types of script classes
        super().__init_subclass__(**kwargs)
        cls.supported_script_objects.append(cls)

@dataclass
class LeaderOpinionModifier(PdxScriptObject):
    """
    Holds data for leader opinion modifiers and allows conversion to PDX script (in the form of economic categories).

    Attributes
    ----------
    name : str
        The 'in-code' name of the opinion modifier.
    value : str
        The numeric value of the opinion modifier.
    localisation: str
        How the opinion modifier is named in game.
    path: Path
        The path to where leader traits are stored (default is modpath/common/economic_categories)
    regex_pattern: re.Pattern
        The regex pattern to use to search for leader opinion modifers. (default is prefix + _leader_opinion)
    script: str
        A snippet of PDX script for a leader opinion modifier in the form of an economic category.
    """
    name: str
    value: str  # TODO maybe make custom datatype
    localisation: str
    path: Path = None  # value assigned post init as it constructed from other attributes
    regex_pattern: re.pattern = None  # value assigned post init as it constructed from other attributes
    script: str = None # value assigned post init as it constructed from other attributes

    def __post_init__(
            self):  # script, path and regex_pattern have to be defined post initalisation because they need the
        # other attributes to be initialized first
        self.script: str = f"""
                    {self.name} = {{
                        #value = {self.value}
                        #localisation = {self.localisation}
                        hidden = yes
                        generate_add_modifiers = {{produces}}
                    }}\n"""
        self.path: Path = Path(self.config["PATHS"]["mod_path"] + "\common\economic_categories")
        self.regex_pattern = re.compile(fr"^{self.prefix}" + "_leader_opinion_")


@dataclass
class LeaderTrait(PdxScriptObject):
    """
    Holds data for leader traits and allows conversion to PDX script

    Attributes
    ----------
    name: str
        The 'in-code' name of the trait.
    cost: int
        The trait cost in trait points.
    modification: str
        Whether the trait counts as a modification (not a bool so it can be parsed directly)
    icon: str
        The path to the trait icon
    modifier: str
        The modifier the trait applies.
    leader_trait: list[str]
        Which leader classes the trait can be applied to.
    leader_class: list[str]
        Which leader classes the trait can be applied to (PDX script uses both this and the above for some reason)
    localisation: str
        How the trait appears ingame.
    path: Path
        The path to where leader traits are stored (default is modpath/common/traits)
    regex_pattern: re.Pattern
        The regex pattern to use to search for leader opinion modifers. (default is prefix + _self.name) #T
    script: str
        A snippet of PDX script for a leader trait

    """

    name: str
    modification: str  # maybe create custom bool with yes no?
    modifier: str
    leader_trait: list[str]
    leader_class: list[str]
    localisation: str
    # fields with default values must be listed last for some reason ?
    cost: int = 0  # default 0
    icon: str = None
    path: Path = None  # value assigned post init as it constructed from other attributes
    regex_pattern: re.pattern = None  # value assigned post init as it constructed from other attributes
    script: str = None  # value assigned post init as it constructed from other attributes

    def __post_init__(self):  # script, path and regex_pattern have to be defined post initialisation because they
        # need the other attributes to be initialized first
        self.script: str = f"""
        {self.name} = {{
            cost = {self.cost}
            modification = {self.modification}
            icon = {self.icon}
            modifier = {{
                {self.modifier}
            }}
            leader_trait = {self.leader_trait}
            leader_class = {{{self.leader_class}}}
        
        }}
        """
        self.path: Path = Path(self.config["PATHS"]["mod_path"] + "\common\\traits")
        self.regex_pattern = re.compile(fr"^{self.prefix}" + "_" + fr"^{self.name}")




# MAIN FUNCTION________________________________________________________________________________________________________
def main():  # maybe move into CustomConfig or a separate functions?
    config = CustomConfig()
    while True:
        try:
            Path("leader_system_config.ini").exists()
            config.read(config_filename)
            config.is_valid()
            print("Config file validation successful.")
            break

        except(FileNotFoundError, InvalidConfigError):
            print("Config file missing or corrupted. Please enter config values.")
            config.get_user_input()
            config.set_config()
            config.write_config_ini()

    # test = LeaderOpinionModifier(name="test", value="test", localisation="test")
    # test2 = LeaderTrait(name="test", modification="no", modifier="test", leader_trait="all", leader_class=["admiral", "envoy"], localisation="test")
    # print(test.script)
    # print(test2.script)

    if["admiral", "scientist"] in

if __name__ == "__main__":
    main()
