#!/usr/bin/python
#################################################################
#
# HAProxy Simple Control Script
#
#  - Script by Jioh L. Jung (zio.zzang@kt.com)
#
#################################################################
# Configuration


"""
* Requirement
  - python 2.6 or above
  - flask
  - netaddr

* Preinstallation
  - must install python-pip
  - PIP install : flask, netaddr
  - Github install: clone git://github.com/neurogeek/haproxyctl.git

* Need same permission with ha-proxy.

* Security
  - IP Allow rule.

* execute
  - [program] -s <socket_path> &

"""

import sys, getopt
import subprocess
import re
import json
from netaddr import IPNetwork, IPAddress
from flask import Flask, redirect, url_for, request, Response

app = Flask(__name__)

# Default Configuration
DEBUG_FLAG = True
LISTEN_PORT = 7777
SOCK = '/var/run/haproxy/haproxy.sock'
ALLOWED_IP_BLOCK = ['192.168.0.0/16', "127.0.0.1/32"]

# Do Argument Parsing
opts, args = getopt.getopt(sys.argv[1:],"s:",["socket="])
for opt, arg in opts:
  if opt in ("-s", "--socket"):
    #print "Set UNIX Socket to '%s'" % arg
    SOCK = arg

# Set Default HAproxy Execution.
def exec_haproxyctl(cmd, backend = "", server = ""):
  global SOCK
  execinfo = ['haproxyctl',
                '-k', SOCK, '-c', cmd
             ]
  if len(backend) > 0:
    execinfo += ['-b', re.escape(backend)]
  if len(server) > 0:
    execinfo += ['-s', re.escape(server)]
  proc = subprocess.check_output(execinfo)

  return proc

# Check Permission.
def check_permission():
  global ALLOWED_IP_BLOCK
  ip = request.remote_addr
  for net in ALLOWED_IP_BLOCK:
    if IPAddress(ip) in IPNetwork(net):
      return True

  print "Permission FAILED."
  return False

@app.route('/')
def cmd_command_list():
  if check_permission() == False:
    return Response(status=403)

  help_msg = """
COMMAND HELP
* Server Status List
URI: /servers/<backend>
Result: Json Format

* Server Enable
URI: /enable/<backend>/<server>
Result: Message only

* Server Disable
URI: /disable/<backend>/<server>
Result: Message only

  """
  return Response(response=help_msg, mimetype="text/plain")

@app.route('/servers/<backend>')
def cmd_servers(backend):
  if check_permission() == False:
    return Response(status=403)

  res = exec_haproxyctl("servers", backend)

  rs = {}
  rl = []
  rexp = re.compile(
      "Name: ([^\:]+)\s+Status: ([a-zA-Z]+)\s+"
      "Weight: ([\d\.]+)\s+bIn: ([\d\.]+)\s+bOut: ([\d\.]+)"
    )

  for line in res.split('\n'):
    matched = rexp.match(line.strip())
    if type(matched) != type(None):
      kv = {}
      kv['name'] = matched.groups()[0]
      kv['status'] = matched.groups()[1]
      kv['weight'] = matched.groups()[2]
      kv['bin'] = matched.groups()[3]
      kv['bout'] = matched.groups()[4]
      rl.append(kv)

  rs['servers'] = rl
  rs['count'] = len(rl)

  return Response(response=json.dumps(rs), mimetype="application/json")

# Activate Server
@app.route('/enable/<backend>/<server>')
def cmd_enable(backend, server):
  if check_permission() == False:
    return Response(status=403)
  res = exec_haproxyctl("enable", backend, server)
  msg = "enable command send OK"
  return Response(response=msg, mimetype="text/plain")

# De-activate Server
@app.route('/disable/<backend>/<server>')
def cmd_disable(backend, server):
  if check_permission() == False:
    return Response(status=403)
  res = exec_haproxyctl("disable", backend, server)
  msg = "disable command send OK"
  return Response(response=msg, mimetype="text/plain")

# No-Page Handler.
@app.errorhandler(404)
def no_page(e):
  # anti-hacking policy
  return Response(status=403)

app.run(debug=DEBUG_FLAG, host='0.0.0.0', port=LISTEN_PORT)
