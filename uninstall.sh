#!/bin/bash
sudo rm -rf /usr/bin/$(cat FINAL_COMMAND_NAME)
sudo rm -rf /var/$(cat FINAL_COMMAND_NAME)
sudo rm -rf /var/$(cat FINAL_COMMAND_NAME)/conf.json