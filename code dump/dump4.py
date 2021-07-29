ethic_opinion_modifiers_positive = ethic_opinion_modifiers_positive + "\n" + prefix + f"""_likes_{ethic} = {{
                            #value = @{prefix}_same_ethic_opinion
                            #name = "{ethic.capitalize()} Government:"
                            hidden = yes
                            generate_add_modifiers = {{
                                produces
                            }}
                        }}\n"""

print("Result:\n" + ethic_opinion_modifiers_positive)

ethic_opinion_modifiers_negative = ethic_opinion_modifiers_negative + "\n" + prefix + f"""_dislikes_{ethic} = {{
                                #value = @{prefix}_opposite_ethic_opinion
                                #name = "{ethic} Government:"
                                hidden = yes
                                generate_add_modifiers = {{
                                    produces
                                }}
                            }}\n"""
ethic_opinion_modifiers_negative
print("Result:\n" + ethic_opinion_modifiers_negative)



@dataclass
class EthicLeaderOpinionModifier(LeaderOpinionModifier):
    script_negative = self.script.replace("same", "opposite").replace("likes", "dislikes")
    """
    Holds data for ethic based leader opinion modifiers and allows conversion to PDX script
    (in the form of economic categories).
    Inherits the generate script method form LeaderOpinionModifier
    """
    def generate_script_negative(self):
        """
        Generate PDX script (economic category used as leader opinion modifier) out of the stored data
        Localisation is adapted to signal dislike towards an ethic.

        Returns
        -------
        script_negative: str
             Snippet of PDX code for a leader opinion modifier, to be used in an economic categories file.
        """
        # replace various text to match disliking an ethic
        script_negative = self.generate_script().replace("same", "opposite").replace("likes", "dislikes")
        return script_negative

    def generate_script_fanatic(self):
        """
        Generate PDX script (economic category used as leader opinion modifier) out of the stored data
        Localisation is adapted to signal a fanatic ethic.

        Returns
        -------
        script_negative: str
             Snippet of PDX code for a leader opinion modifier, to be used in an economic categories file.
        """
        # replace various text to match fanatic ethics
        script_fanatic = self.generate_script().replace("likes_", "likes_fanatic_").replace("_opinion","_opinion_fanatic")
        script_fanatic = re.sub(r"(?<=#localisation = ).*", f"Fanatic {self.localisation}", self.script_fanatic)
        return script_fanatic
