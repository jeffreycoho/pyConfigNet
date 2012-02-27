# -*- coding: utf-8 -*-

import sys,os

def cmdNoxCore(noxPort, noxType):
    cmdString = 'cd /usr/local/src/RouteFlow/rf-controller/build/src;' + \
            './nox_core -v -i ptcp:' + str(noxPort) + \
            ' ' + noxType + ' -d'
    os.system(cmdString)
    print cmdString    


def runRfServer():
    cmdString = '''./usr/local/src/RouteFlow/build/rf-server &'''
    os.system(cmdString)
    print cmdString

def cmdLxcStart(name):
    cmdString = '''lxc-start -n ''' + name + ''' -d''';
    os.system(cmdString)
    print cmdString

def cmdOvsOpenflowd(name, ip, port, hw_desc = None):
    if(hw_desc):
        cmdString = '''ovs-openflowd --hw-desc='''+ hw_desc + \
                    ' ' + name +'  tcp:' + ip + ':' + str(port) + \
                    ''' --out-of-band --detach'''
    else:
        cmdString = '''ovs-openflowd ''' + name + ' tcp:' + \
                    ip + ':' + str(port) + \
                    ''' --out-of-band --detach'''
    
    os.system(cmdString)
    print cmdString

def cmdIfconfig(interface, action, ip = None, netmask = None):
    if(ip and netmask):
        cmdString = 'ifconfig ' + interface + ' ' + action + \
                    ' ' + ip + ' netmask ' + netmask
    else:
        cmdString = 'ifconfig ' + interface + ' ' + action

    os.system(cmdString)
    print cmdString


def cmdOvsDpctl(entity, interface, action = 'add-if'):
    cmdString = 'ovs-dpctl ' + action + ' ' + entity + \
                ' ' + interface
    os.system(cmdString)
    print cmdString



if __name__ == '__main__':
    cmdNoxCore(6363, 'switch')
    cmdNoxCore(6633, 'routeflowc')
    runRfServer()
    cmdLxcStart('router1')
    cmdLxcStart('router2')
    cmdLxcStart('b1')
    cmdLxcStart('b2')
    cmdOvsOpenflowd('dp0', '127.0.0.1', 6633, 'rfovs')
    cmdIfconfig('dp0', 'up')
    cmdOvsOpenflowd('br0', '127.0.0.1', 6363)
    cmdIfconfig('br0', 'up', '192.168.1.1', '255.255.255.0')

    dp0Interface = ['router1.1', 'router1.2', 'router2.1', 'router2.2']
    for interface in dp0Interface:
        cmdOvsDpctl('dp0', interface)

    br0Interface = ['router1.0', 'router2.0']
    for  interface in br0Interface:
        cmdOvsDpctl('br0', interface)

    cmdOvsOpenflowd('switch1', '127.0.0.1', 6633)
    cmdOvsOpenflowd('switch2', '127.0.0.1', 6633)

    switch1Interface = ['b1.0', 'eth2']
    switch2Interface = ['eth3', 'b2.0']
    for interface in switch1Interface:
        cmdOvsDpctl('switch1', interface)
    for interface in switch2Interface:
        cmdOvsDpctl('switch2', interface)

