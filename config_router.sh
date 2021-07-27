#!/bin/bash

ip address add 10.0.0.1/8 dev eno1
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -j MASQUERADE

