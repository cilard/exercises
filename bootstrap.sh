#!/usr/bin/env bash

apt-add-repository -y ppa:ansible/ansible
apt-get update
apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev ansible
pip3 install --upgrade pip
cat << EOF > /etc/default/locale
LANG=en_US.UTF-8
LC_CTYPE="en_US.UTF-8"
LC_ALL="en_US.UTF-8"
EOF

