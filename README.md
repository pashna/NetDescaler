# Network Downscaler

The tool is an implementation of the idea proposed in the article 
> Kim, Hwangnam, Hyuk Lim, and Jennifer C. Hou. Network Invariant-Based Fast Simulation for Large Scale TCP/IP Networks. 2004.

but with using fast prototyping (based on Mininet) rather than simulation, which helps to improve accurancy of the method.

## How to use the app
*0. Install all the dependency*

1. Define network configuration in config.py. 
* *scale_factor* is a number from 0 to 1 
* *save_path* is a folder where tcpdumps transformed into csv-files will be stored
* *hosts* list of hosts
* *switches* list of switches
* *links* list of links with theirs parameters (*Bandwidth, delay*)
* *commands* field is what will be running on the given host after sleep time and it is supposed to run network application. User may want to use the apps from our library *NetworkApps* (like FTP server, FTP client, HTTP-server, HTTP-client), built-in linux apps (like *AB, curl*, etc.) or use traffic generator ([D-ITG](http://www.grid.unina.it/software/ITG/) is the best fit)

2. Run the app
```
sudo python main.py
```
and wait until the emulation finishes.

3. For result visualization we use [bowtie](https://github.com/jwkvam/bowtie), so one needs to install it prior running the visualization module. After the installation
```
python visualization.py build
python visualization.py serve
```
and the visualization will be avaliable via the link https://localhost:9991
