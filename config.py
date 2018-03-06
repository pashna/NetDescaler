
CONFIG = \
    {     "scale_factor": 0.5,
          "plot_graph": True,
          'interface_to_capture': ['s1-eth1'],
          "save_path": "/home/pkochetk/msu/diploma/repo/csv/",
          "hosts": ["h1", "h2", "h3", "h4"],
          "switches": ["s1"],

          "links": [
          {
              "node1": "h1",
              "node2": "s1",
              "bw": 20,
              "delay": "10ms",
          },
          {
              "node1": "h2",
              "node2": "s1",
              "bw": 20,
              "delay": "10ms",
          },
          {
              "node1": "h3",
              "node2": "s1",
              "bw": 20,
              "delay": "10ms",
          },
          {
              "node1": "h4",
              "node2": "s1",
              "bw": 20,
              "delay": "10ms",
          },
          ],
          "commands": {
              "h1": [{"cmd": "python NetworkApps/ftp/ftp_server.py",
                      "sleep_time": 0}],
              "h2": [{"cmd": "python NetworkApps/ftp/ftp_client.py 50M h1 download",
                      "sleep_time": 1}],
              "h3": [{"cmd": "python NetworkApps/ftp/ftp_client.py 50M h1 download",
                      "sleep_time": 2}],
              "h4": [{"cmd": "python NetworkApps/ftp/ftp_client.py 50M h1 download",
                      "sleep_time": 2}],

          }
}