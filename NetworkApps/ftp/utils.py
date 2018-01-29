import subprocess

def get_ip():
    proc = subprocess.Popen(["ifconfig | grep -Po '(?<=inet addr:)[0-9\.]+'"], stdout=subprocess.PIPE, shell=True)
    out, _ = proc.communicate()
    ip_address = str(out).split('\\n')[0][2:]
    return ip_address