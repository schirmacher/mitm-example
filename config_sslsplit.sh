#!/bin/bash

iptables -t nat -F
iptables -t nat -A POSTROUTING -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443
rm -f logdir/*
mkdir -p /tmp/sslsplit
sslsplit -D -l connect.log  -j /tmp/sslsplit/ -S logdir/ -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080

