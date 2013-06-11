haproxy-webctl
==============
HAProxy Web Controller
Control HAProxy with no stopping current service.


Author
======
Script by Jioh L. Jung (ziozzang@gmail.com)

Requirement
===========
python 2.6 or above
- flask (pip)
- netaddr (pip)
- haproxyctl (GitHub)


Installation
============
- must install python-pip
- PIP install : flask, netaddr
- Github install: clone git://github.com/neurogeek/haproxyctl.git

- Need same permission with ha-proxy.

* configuration

HA-Proxy configuration
/etc/haproxy/haproxy.cfg

```
global
  # socket is mandatory for haproxy-webctl.
  stats socket /var/run/haproxy/haproxy.sock mode 0600 level admin
backend portal # this backend name is used for API request.
  #default-server on-error mark-down fall 1 error-limit 1

```

* Install Script

```
apt-get install -fy python-pip
pip install flask netaddr

cd ~/
git clone git://github.com/neurogeek/haproxyctl.git
cd haproxyctl/
python setup.py install

cd ~/
git clone git://github.com/ziozzang/haproxy-webctl.git
```

* Configuration of API Server.
You can fix environment for UNIX Socket (SOCK), listen port(LISTEN_PORT) and Listening IP.

Security
========
* IP Allow rule.

you can edit IP allow rule in script. if client ip has not in list, they get 403(No Permission) Error.

```
ALLOWED_IP_BLOCK = ['IP/mask', '....']
```

Execute
=======
* Run as same account with haproxy.

```
[program] -s <socket_path> -p <port_number> &
```

* API Usage

if server address is 1.2.3.4:7777 , you can use API like this.

* Request for status of backend which name is 'backend_name'

```
curl http://1.2.3.4:7777/servers/backend_name
```

You can get JSON format of backend servers status.

* Request for server_name enable(UP Status) on backend_name

```
curl http://1.2.3.4:7777/enable/backend_name/server_name
```

this can only do request, doesn't show status of backend or server.

* Request for server_name disable(MAINTAINANCE Status) on backend_name

```
curl http://1.2.3.4:7777/disable/backend_name/server_name
```

this can only do request, doesn't show status of backend or server.
