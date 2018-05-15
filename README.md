# Network Downscaler

The tool is an implementation of the idea proposed in the article 
> Kim, Hwangnam, Hyuk Lim, and Jennifer C. Hou. Network Invariant-Based Fast Simulation for Large Scale TCP/IP Networks.

but using fast prototyping (based on Mininet) rather than simulation, which helps to improve accurancy of the method.

## How to use the app
### Installation
1. Install [Mininet](http://mininet.org/) or use provided vm-image. 
2. For result visualization we use [bowtie](https://github.com/jwkvam/bowtie), so one needs to install it prior running the visualization module.

### Usage
Define network configuration in *config.py*.
* *scale_factor* is a number from 0 to 1 
* *save_path* is a folder where tcpdumps transformed into csv-files will be stored
* *plot_graph* set as True if before running the experiment you want to have a visialization of your topology
* *hosts* list of hosts
* *switches* list of switches
* *links* list of links with theirs parameters (*Bandwidth, delay*)
* *commands* field is what will be running on the given host after sleep time and it is supposed to run network application. User may want to use the apps from our library *NetworkApps* (like FTP server, FTP client, HTTP-server, HTTP-client), built-in linux apps (like *AB, curl*, etc.) or use traffic generator ([D-ITG](http://www.grid.unina.it/software/ITG/) is the best fit)

There is two options to use it.

1.
```
python WebInterface.py build
python WebInterface.py serve
```

This will run a server, available on https://localhost:9991
The experiment can be ran by apploading a config.

Although, if at least one of the applications doesn't finish (usually, it happends to servers), the experiment will
be frozen and the results won't show off. In this case, you can interrupt the execution any time. pcap files still
will be available in csv folder, and can be analyzed by wireshark, but the user must take into account the fact that it
was scaled up by scale factor, which made all the events delayed.


For standalone experiment result (csv) visualization, that will take care of
```
python WebInterface.py build
python WebInterface.py serve
```


1. Run the app
```
sudo python main.py
```
and wait until the emulation finishes.

2. Folder csv will contain csv- and pcap-files from

Visualize the result
```
python WebInterface.py build
python WebInterface.py serve
```
and the graphs will be avaliable via the link https://localhost:9991
