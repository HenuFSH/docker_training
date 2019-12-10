#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import commands
import ipaddress

def execting_command(command):
    print(command)
    return command
    # status, output = commands.getstatusoutput(command)
    # if status != 0:
    #     print("Exrcting command %s failed.", command)
    # else:
    #     return output

def set_iptable(export_ip, container_ip):
    execting_command('iptables -t nat -A PREROUTING -d {} -j DNAT --to-destination {}'.format(export_ip, container_ip))
    execting_command('iptables -t nat -A POSTROUTING -d {} -j SNAT --to {}'.format(container_ip, export_ip))

def crate_network_alias(export_ip):
    execting_command('ifconfig enp2s0:0 {} netmask 255.255.255.0 up'.format(export_ip))

def get_container_ip(container):
    return execting_command('docker inspect -f "{{.NetworkSettings.IPAddress}}" {}'.format(container))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Export the ip for docker container.")
    parser.add_argument('--name', '-n')
    parser.add_argument('--id', '-id')
    parser.add_argument('--ip', '-i')
    args = parser.parse_args()

    if not (args.name or args.id):
        print('Name or ID is required.')

    container = args.name if args.name else args.id
    container_ip = get_container_ip(container)
    export_ip = args.ip

    crate_network_alias(export_ip)
    set_iptable(export_ip, container_ip)