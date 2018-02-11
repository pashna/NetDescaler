
CONFIG = {
          "scale_factor": 0.5,
          "save_path": "/home/pkochetk/images/data/MSU/capture/csv/0_5/",
          "plot_graph": True,
          "hosts": ["h1", "h1_1", "h1_2",
                    "h2", "h2_1", "h2_2",
                    "h3", "h3_1", "h3_2", ],
          "switches": ["s1", "s2", "s3", "s4", "s5"],
          "links": [
          {
              "node1": "h1_1", "node2": "s1",
              "bw": 10, "delay": "10ms",
          },
          {
              "node1": "h1_2", "node2": "s1",
              "bw": 10, "delay": "10ms",
          },


          {
              "node1": "h2_1", "node2": "s2",
              "bw": 10, "delay": "10ms",
          },
          {
              "node1": "h3_1", "node2": "s3",
              "bw": 10, "delay": "10ms",
          },


          {
              "node1": "h2", "node2": "s3",
              "bw": 10, "delay": "10ms",
          },


          {
              "node1": "h3", "node2": "s4",
              "bw": 10, "delay": "10ms",
          },

          {
              "node1": "h1", "node2": "s5",
              "bw": 10, "delay": "10ms",
          },



          {
              "node1": "s1", "node2": "s2",
              "bw": 10, "delay": "10ms",
          },
          {
              "node1": "s2", "node2": "s3",
              "bw": 10, "delay": "10ms",
          },
          {
              "node1": "s3", "node2": "s4",
              "bw": 10, "delay": "10ms",
          },
          {
              "node1": "s4", "node2": "s5",
              "bw": 10, "delay": "10ms",
          }
          ],
          "commands": {
              "h1": [{"cmd": "python NetworkApps/ftp/ftp_server.py",
                      "sleep_time": 0}],
              "h2": [{"cmd": "python NetworkApps/ftp/ftp_server.py",
                                      "sleep_time": 0}],
              "h3": [{"cmd": "python NetworkApps/ftp/ftp_server.py",
                                      "sleep_time": 0}],


              "h1_1": [{"cmd": "python NetworkApps/ftp/ftp_client.py 10M h1 download",
                      "sleep_time": 0}],
              "h1_2": [{"cmd": "python NetworkApps/ftp/ftp_client.py 10M h1 download",
                      "sleep_time": 0}],


              "h2_1": [{"cmd": "python NetworkApps/ftp/ftp_client.py 10M h2 download",
                      "sleep_time": 0}],
              "h2_2": [{"cmd": "python NetworkApps/ftp/ftp_client.py 10M h2 download",
                      "sleep_time": 0}],


              "h3_1": [{"cmd": "python NetworkApps/ftp/ftp_client.py 10M h3 download",
                      "sleep_time": 0}],
              "h3_2": [{"cmd": "python NetworkApps/ftp/ftp_client.py 10M h3 download",
                      "sleep_time": 0}],
          }
}