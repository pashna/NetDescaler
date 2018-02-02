import re

class BDProduct:

    def __init__(self, scaling_factor):
        self.__scaling_factor = scaling_factor

    def update_config(self, config):
        print("Updating config...")
        for link_conf in config["links"]:
            delay = re.findall(r'\d+', link_conf["delay"])[0]
            dim = link_conf["delay"].replace((str(delay)), "")
            delay = int(round(float(delay) / self.__scaling_factor))
            link_conf["delay"] = "{}{}".format(delay, dim)
            link_conf["bw"] = int(round(link_conf["bw"] * self.__scaling_factor))

        for h, commands in config["commands"].items():
            for cmd in commands:
                cmd["sleep_time"] /= self.__scaling_factor

        print("Config is updated")
        return config