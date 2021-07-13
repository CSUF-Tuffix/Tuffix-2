#!/usr/bin/env bash

# AUTHOR: Jared Dyreson
# Project: Tuffix Testing

# NOTE: mount device from panel first before continuing

# install deps

sudo apt-get install build-essentials dkms linux-headers-"$(uname -r)"

# install the additions

sudo su
cd /media
mkdir cdrom
mount /dev/cdrom /media/cdrom
cd cdrom
sh VBoxLinuxAdditions.run

# NOTE: you can delete the following lines if you want
# Point Person: Jared Dyreson

# install zsh and other ammenities

sudo apt-get -y install zsh vim

ZSHRC_LINK=""
VIMRC_LINK=""
