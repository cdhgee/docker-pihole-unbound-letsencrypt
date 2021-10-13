#!/usr/bin/python3

import os
import re
import ipaddress

def secret_input(prompt):
  
  os.system('stty -echo')
  result = input(prompt)
  os.system('stty echo')
  print('\n')
  return result

def get_default_file(srcfile):

  with open(srcfile, 'r') as src:
    lines = src.readlines()

  return lines

def replace_placeholders(lines, search, replace):
  
  for line in lines:
    line = re.sub(search, replace, l)

  return lines

def save_processed_file(destfile, lines):

  with open(destfile, 'w') as dest:
    for line in lines:
      dest.write(line)
  
def process_default_file(srcfile, destfile, replacements):

  lines = get_default_file(srcfile)

  for k in replacements:
    lines = replace_placeholders(lines, k, replacements[k]

  save_processed_file(destfile, lines)
  
envs = {}

envs['WEBPASSWORD'] = secret_input('Enter a password for the Pi-hole web UI: ')

envs['HOSTNAME'] = input('Enter a hostname or FQDN for the Pi-hole web UI: ')


apitoken = secret_input('Enter the Cloudflare API token: ')

zoneid = secret_input('Enter the Cloudflare zone ID: ')

envs['SUBNETv4'] = input('Enter the IPv4 subnet: ')
envs['GWv4'] = input('Enter the IPv4 gateway: ')
envs['SUBNETv6'] = input('Enter the IPv6 subnet: ')
envs['GWv6'] = input('Enter the IPv6 gateway: ')

stringOffset = input('Enter the IP offset for this Pi-hole [0]: ')
if stringOffset == '':
  stringOffset = '0'

envs['INTERFACE'] = input('Enter the parent interface to use: ')

offset = int(stringOffset)

ipv4network = ipaddress.IPv4Network(envs['SUBNETv4'])
ipv6network = ipaddress.IPv6Network(envs['SUBNETv6'])
envs['PIHOLE_IPv4'] = ipv4network[10 + offset].compressed
envs['PIHOLE_IPv6'] = ipv6network[16 + offset].compressed
envs['LETSENCRYPT_IPv4'] = ipv4network[20 + offset].compressed
envs['LETSENCRYPT_IPv6'] = ipv6network[32 + offset].compressed

with open('.env', 'w') as f:
  for e in envs:
    f.write(f'{e}={envs[e]}\n')


os.mkdir('./letsencrypt/live')
os.mkdir('./letsencrypt/archive')
os.mkdir('./dnsmasq')

process_default_file('lighttpd/external.conf.default', 'lighttpd/external.conf', {'--HOSTNAME': hostname})
process_default_file('dnsrobocert/config.yml.default', 'dnsrobocert/config.yml', {'--CLOUDFLARETOKEN--': apitoken, '--CLOUDFLAREZONEID--', zoneid})

