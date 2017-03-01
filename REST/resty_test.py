import os
import sys

os.chdir('/root/python/Python-Colletcions')
if '/root/python/Python-Colletcions' not in sys.path:
    sys.path.append('/root/python/Python-Colletcions')

import time
from utils.system_usage import cpu_usage, mem_usage, disk_usage

_hello_resp = '''\
<html>
  <head>
     <title>Hello {name}</title>
   </head>
   <body>
     <h1>Hello {name}!</h1>
   </body>
</html>'''

def hello_world(environ, start_response):
    start_response('200 OK', [ ('Content-type','text/html')])
    params = environ['params']
    resp = _hello_resp.format(name=params.get('name'))
    yield resp.encode('utf-8')

_localtime_resp = '''\
<?xml version="1.0"?>
<time>
  <year>{t.tm_year}</year>
  <month>{t.tm_mon}</month>
  <day>{t.tm_mday}</day>
  <hour>{t.tm_hour}</hour>
  <minute>{t.tm_min}</minute>
  <second>{t.tm_sec}</second>
</time>'''

def localtime(environ, start_response):
    start_response('200 OK', [ ('Content-type', 'application/xml') ])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')


_json_resp ={'HostName':0,
        'CPU':0,
        'MEM':0,
        'DISK':0
}

def sys_usage(environ, start_response):
    import json
    start_response('200 OK', [ ('Content-type', 'text/json') ])
    _json_resp['HostName'] = 'xubutu'
    _json_resp['CPU'] = cpu_usage()
    _json_resp['MEM'] = mem_usage()
    _json_resp['DISK'] = disk_usage()
    print _json_resp
    resp = json.dumps(_json_resp)
    yield resp.encode('utf-8')

def sublime_channel(environ, start_response):
    import json
    start_response('200 OK', [ ('Content-type', 'text/json') ])
    with open('/root/python/Python-Colletcions/REST/data/channel_v3.json') as fp:
        resp = ''.join(fp.readlines())
    yield resp.encode('utf-8')

if __name__ == '__main__':
    from REST.resty import PathDispatcher
    from wsgiref.simple_server import make_server

    # Create the dispatcher and register functions
    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', localtime)
    dispatcher.register('GET', '/sys_usage', sys_usage)
    dispatcher.register('GET', '/channel_v3.json', sublime_channel)

    # Launch a basic server
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()
