from datetime import datetime, timedelta
from functools import reduce

class FlowScheduler:

    def __init__(self, delta_sec=10):
        self.__start_at = datetime.now() + timedelta(seconds=delta_sec)

    def get_host_ip(self, net):
        ip_addresses = {}
        for h in net.hosts:
            host_name = h.name
            ip_addresses[host_name] = h.cmd("ifconfig {}-eth0 | grep -Po '(?<=inet addr:)[0-9\.]+'".format(host_name))[:-2]

        return ip_addresses

    def run_commands(self, net, config):
        ip_addresses = self.get_host_ip(net)
        print(ip_addresses)
        for h in net.hosts:
            if h.name in config:
                cmd_configs = config[h.name]
                for cmd_config in cmd_configs:
                    cmd = cmd_config["cmd"]
                    sleep_time = cmd_config["sleep_time"]

                    sleep_time = (self.__start_at - datetime.now()).total_seconds() + sleep_time
                    cmd = cmd + " " + str(sleep_time)

                    cmd = reduce(lambda x, y: x.replace(y, ip_addresses[y]), ip_addresses, cmd)
                    print(cmd)

                    if 'server' in cmd:
                        cmd += " &"
                    h.startShell()
                    h.sendCmd(cmd)
                    h.waiting = True

        from time import sleep
        sleep(10)
        print("All flows are started")
        results = {}

        for h in net.hosts:
            results[h.name] = h.waitOutput()

        return results
