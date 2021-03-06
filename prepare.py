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

def save_processed_file(destfile, lines):

  with open(destfile, 'w') as dest:
    for line in lines:
      dest.write(line)
  
def process_default_file(srcfile, destfile, replacements):

  lines = get_default_file(srcfile)

  for i, s in enumerate(lines):
    lines[i] = re.sub('--(\w+)--', lambda m: replacements.get(m.group(1), m.group(0)), lines[i])

  save_processed_file(destfile, lines)
  
envs = {}

envs['WEBPASSWORD'] = secret_input('Pi-hole web UI password: ')

envs['HOSTNAME'] = input('Pi-hole web UI hostname or FQDN: ')


apitoken = secret_input('Cloudflare API token: ')

zoneid = secret_input('Cloudflare zone ID: ')

envs['SUBNETv4'] = input('IPv4 subnet: ')
envs['GWv4'] = input('IPv4 gateway: ')
envs['SUBNETv6'] = input('IPv6 subnet: ')
envs['GWv6'] = input('IPv6 gateway: ')

stringOffset = input('IP offset for this Pi-hole [0]: ')
if stringOffset == '':
  stringOffset = '0'

envs['INTERFACE'] = input('Parent interface to use: ')

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

basedir = os.path.join(os.path.dirname(__file__))

def mkdirp(path):
  try:
    os.makedirs(path)
  except:
    pass

mkdirp(f'{basedir}/letsencrypt/live')
mkdirp(f'{basedir}/letsencrypt/archive')
mkdirp(f'{basedir}/dnsmasq')

process_default_file('lighttpd/external.conf.default', 'lighttpd/external.conf', {'HOSTNAME': envs['HOSTNAME']})
process_default_file('dnsrobocert/config.yml.default', 'dnsrobocert/config.yml', {'CLOUDFLARETOKEN': apitoken, 'CLOUDFLAREZONEID': zoneid})

