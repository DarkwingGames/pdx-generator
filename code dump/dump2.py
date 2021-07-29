
def read_config():
    """Reads the configuration file, raises and informs the user if it doesn't exist"""
    print("Reading Configuration...")
    config_file = Path('leader_system_config.ini')

    if config_file.exists():
        config_parser.read("leader_system_config.ini")
        config_dict = {sect: dict(config_parser.items(sect)) for sect in config_parser.sections()}
        return config_dict
    else:
        print("Configuration file could not be read or was not found. Please enter configuration values as prompted.")
        create_config()
        config_dict = {sect: dict(config_parser.items(sect)) for sect in config_parser.sections()}
        return config_dict


    def __init__(self, generate_negative=True, generate_fanatic=True, *args, **kwargs):
        super(EthicOpinionModifier, self).__init__(*args, **kwargs)
        self.generate_negative = generate_negative
        self.generate_fanatic = generate_fanatic
        if generate_negative:
            self.script = self.script + self.script.replace("same", "opposite").replace("likes", "dislikes")

        if generate_fanatic:
            self.pdx_script_fanatic = self.script.replace("likes_", "likes_fanatic_").replace("_opinion", "_opinion_fanatic")
            self.pdx_script_fanatic = re.sub(r"(?<=#localisation = ).*", f"Fanatic {self.localisation}", self.pdx_script_fanatic)
            self.script = self.script + self.pdx_script_fanatic



def read_config():
    """Reads the configuration file, raises and informs the user if it doesn't exist"""
    print("Reading Configuration...")
    config_file = Path('leader_system_config.ini')

    if config_file.exists():
        config.read("leader_system_config.ini")
        config_dict = {sect: dict(config.items(sect)) for sect in config.sections()}
        return config_dict
    else:
        print("Configuration file could not be read or was not found. Please enter configuration values as prompted.")
        create_config()
        config_dict = {sect: dict(config.items(sect)) for sect in config.sections()}
        return config_dict


def create_ethic_modifiers(config_dict):
    ethics_folder = "\common\ethics"
    prefix = config_dict["PREFIX"]["prefix"]
    search_pattern_ethics = re.compile(r"-?\nethic_([^fanatic]\w+)")
    search_pattern_ethics_mod = re.compile(r"-?\nspo_ethic_([^fanatic]\w+)")  # For some reason the regex pattern used for vanilla doesn't work here
    ethic_opinion_modifiers = ""

    if bool(config_dict["SETTINGS"]["generate_ethics"]):
        print("Processing ethics...")
        while True:
            if "vanilla_path" in config_dict["PATHS"] and Path(config_dict["PATHS"]["vanilla_path"] + ethics_folder).exists() == True and Path(config_dict["PATHS"]["mod_path"] + ethics_folder).exists() == True:
                vanilla_ethics = Path(config_dict["PATHS"]["vanilla_path"] + ethics_folder)
                mod_ethics = Path(config_dict["PATHS"]["mod_path"] + ethics_folder)
                for file in vanilla_ethics.glob('*.txt'):
                    f = file.read_text()
                    ethics = re.findall(search_pattern_ethics, f)
                    print(ethics)

                for file in mod_ethics.glob('*.txt'):
                    f = file.read_text()
                    mod_ethics = re.findall(search_pattern_ethics_mod, f)
                    #print(f)
                    print(ethics)

                for ethic in ethics:
                    modifier = EthicOpinionModifier(name=f"{prefix}_likes_{ethic}", localisation=f"{ethic}:".capitalize(), value="@same_ethic_opinion")
                    ethic_opinion_modifiers = ethic_opinion_modifiers + modifier.script
                #print(ethic_opinion_modifiers)


                break

            else:
                update_vanilla_path = input("Vanilla ethics not found. Please specify the correct path: ")
                config["PATHS"]["vanilla_path"] = update_vanilla_path
                with open('leader_system_config.ini', 'w') as conf:
                    config.write(conf)
                config_dict = read_config()

        return vanilla_ethics