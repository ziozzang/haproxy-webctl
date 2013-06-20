# -*- coding: UTF-8 -*-
# This configuration is Python script.

# if you want to display verbose mode of execution set True. else, set False
DEBUG_FLAG = True

# Listening port.
LISTEN_PORT = 7777

# HAProxy UNIX-Socket name
SOCK = '/var/run/haproxy/haproxy.sock'

# only this ip block is allowed
ALLOWED_IP_BLOCK = [
  '192.168.0.0/16',
  "127.0.0.1/32"
]

