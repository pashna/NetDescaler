
CONFIG = \
    {
          "interfaces_to_capture": ["h1", "h2"],
          "hosts": ["h1", "h2", "h3", "h4"],
          "switches": ["s1", "s2"],
          "links": [
          {
              "node1": "h1",
              "node2": "s1",
              "bw": 10,
              "delay": "5ms",
          },
          {
              "node1": "h2",
              "node2": "s1",
              "bw": 10,
              "delay": "5ms",
          },
          {
              "node1": "h3",
              "node2": "s2",
              "bw": 10,
              "delay": "5ms",
          },
          {
              "node1": "h4",
              "node2": "s2",
              "bw": 50,
              "delay": "5ms",
          },
          {
              "node1": "s1",
              "node2": "s2",
              "bw": 50,
              "delay": "5ms",
          },
          ],
          "commands": {
              "h1": [{"cmd": "python NetworkApps/ftp/ftp_server.py",
                      "sleep_time": 0}],
              "h2": [{"cmd": "python NetworkApps/ftp/ftp_client.py 50M h1 download",
                      "sleep_time": 0}],
              "h3": [{"cmd": "python NetworkApps/ftp/ftp_client.py 50M h1 download",
                      "sleep_time": 0}],
              "h4": [{"cmd": "python NetworkApps/ftp/ftp_client.py 50M h1 download",
                      "sleep_time": 0}],

          }
}