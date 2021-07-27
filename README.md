# mitm-example
Configuration for sslsplit / sslproxy and python script to process https traffic

The config_router.sh script configures a Linux system as a router. It adds a new network interface with the ip address 10.0.0.1 and netmask of 255.0.0.0.

To send all traffic from another PC through this Linux system to the internet, enter the IP address of that interface into the manual network configuration as the default gateway and assign a new ip address, for example 10.0.0.2, as the ip address of the PC. After that, all traffic from and to the PC will be routed through the Linux system.

The config_sslsplit.sh script sets up the sslsplit program with some reasonable defaults and changes the network configuration so that any traffic is send to sslsplit, which writes all data into log files before sending it to the actual destination. It will also decrypt https traffic, so the log files will contain the plain text of any https and other encrypted data transfers. See the sslsplit project for documentation on how to create the ca.key and ca.crt files and all other aspects of the sslsplit program.

The log files found in the logdir directory contain all data from each connection. The specific program I want to analyze uses json and brotli compression so that's what I have implemented in the decodetraffic.py script.

Finally, there is a rudimentary inspectjson.py script that reads in the json files written by decodetraffic.py . 
