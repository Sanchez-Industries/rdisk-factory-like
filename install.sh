#!/bin/bash
sudo cp rdisk-flike.py /usr/bin/$(cat FINAL_COMMAND_NAME)
sudo chmod a+x /usr/bin/$(cat FINAL_COMMAND_NAME)
sudo mkdir -p /var/$(cat FINAL_COMMAND_NAME)
sudo cp uninstall.sh /var/$(cat FINAL_COMMAND_NAME)/uninstall.sh
sudo chmod a+x /var/$(cat FINAL_COMMAND_NAME)/uninstall.sh
sudo cp conf.json /var/$(cat FINAL_COMMAND_NAME)/conf.json