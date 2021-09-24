#!/bin/bash

echo -n "Enter a password for the Pi-hole web UI: "
read -s WEBPASSWORD
echo

echo WEBPASSWORD=$WEBPASSWORD > .env

echo -n "Enter a hostname for the Pi-hole: "
read HOSTNAME
echo

echo HOSTNAME=$HOSTNAME >> .env

echo -n "Enter the cloudflare API token: "
read APITOKEN
echo

echo -n "Enter the cloudflare zone ID: "
read ZONEID

mkdir -p ./letsencrypt/live
mkdir -p ./letsencrypt/archive
mkdir -p ./dnsmasq

sed -e "s/--HOSTNAME--/$HOSTNAME/g" lighttpd/external.conf.default > lighttpd/external.conf
sed -e "s/--HOSTNAME--/$HOSTNAME/g" -e "s/--CLOUDFLARETOKEN--/$APITOKEN/g" -e "s/--CLOUDFLAREZONEID--/$ZONEID/g" dnsrobocert/config.yml.default > config.yml.
